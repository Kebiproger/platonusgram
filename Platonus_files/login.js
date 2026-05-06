var isFieldExist = function (fieldName) {
    return document.getElementById(fieldName);
};
function onSubmit() {
    var edsUsed = document.getElementById('edsUsed') != null && document.getElementById('edsUsed').value == "true";
   if (!edsUsed) {
       var loginRadioChecked = document.getElementById('loginRadio') != null && document.getElementById('loginRadio').value == "1";
       var iinRadioChecked = document.getElementById('loginRadio') != null && document.getElementById('loginRadio').value == "2";

       if (!iinRadioChecked && document.getElementById('login_input') && document.getElementById("login_input").value.length == 0) {
            return false;
        }
        if (!loginRadioChecked && document.getElementById('iin_input') && document.getElementById("iin_input").value.length == 0) {
            return false;
        }
        if (document.getElementById("pass_input").value.length == 0) {
            return false;
        }
    }

    var authForDeductedStudentsAndGraduates = false;
    if (document.getElementById('authForDeductedStudentsAndGraduates') != null) {
        authForDeductedStudentsAndGraduates = document.getElementById('authForDeductedStudentsAndGraduates').value;
        authForDeductedStudentsAndGraduates = authForDeductedStudentsAndGraduates != null && authForDeductedStudentsAndGraduates == "true";
    }
    localStorage.authForDeductedStudentsAndGraduates = authForDeductedStudentsAndGraduates;

    var languageSelect = document.getElementById("language");
    if (languageSelect) {
        localStorage.language = languageSelect.value;
    }

    blockUIStart();

    if (edsUsed) {
        loginWithEds(0)
    } else {
        loginWithoutEds()
    }
}

function loginWithEds(personRoleType) {
    localStorage.signedXml = localStorage.signedXml != null ? localStorage.signedXml : document.getElementById('signedXml').value;
    $.ajax({
        url: 'rest/api/login/eds',
        type: 'GET',
        beforeSend: function(request) {
            request.setRequestHeader("language", localStorage.language ? localStorage.language : 0);
        },
        data: jQuery.param({
            certificate: localStorage.signedXml,
            personRoleType: personRoleType,
            authForDeductedStudentsAndGraduates: localStorage.authForDeductedStudentsAndGraduates
        }) ,
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        success: function (responseJson) {
            blockUIStop();

            var response = JSON.parse(responseJson);

            if (response.personRoleTypes != null && response.personRoleTypes.length > 0) {
                openChoosePersonRoleDialog(response.personRoleTypes);
            } else {
                if (response.login_status == 'success') {
                    localStorage.signedXml = null;
                    localStorage.token = response.auth_token;
                    localStorage.uid = response.uid;
                    localStorage.sid = response.sid;
                    document.location.href = 'login' + window.location.search;
                }
            }
        },
        error: function (error) {
            blockUIStop();
            clearEdsFields();

            if(error.responseText && error.responseText){
                ToastMessage.error(JSON.parse(error.responseText).message);
            }
        }
    });
}

function openChoosePersonRoleDialog(personRoleTypes) {
    let html = '';

    for (let personRoleType of personRoleTypes) {
        html += '<div class="radio"><input type="radio" id="personRoleType_' + personRoleType + '" value="' + personRoleType + '">' +
            '<label onclick="loginWithEds('+ personRoleType + ')" for="personRoleType_' + personRoleType + '">' + getPersonRoleTypeName(personRoleType) + '</label>' +
            '</div>';
    }

    document.getElementById('personRolesBlock').innerHTML = html;
    document.getElementById('personRoleDialogHeader').innerHTML = getLocalised('Жүйеге авторизация жасайтын рөлді таңдаңыз', 'Выберите роль, под которой вы хотите авторизоваться', 'Select the role you want to log in to');

    $('#selectPersonRole').modal('show');
}

function getPersonRoleTypeName(personRoleType) {
    switch (personRoleType) {
        case 1:
            return getLocalised('Білім алушы', 'Обучающиеся', 'Student');
        case 3:
            return getLocalised('Оқытушы', 'Преподаватель', 'Tutor');
        case 38:
            return getLocalised('Ата-ана', 'Родитель', 'Parent');
    }
}

function getLocalised(nameKz, nameRu, nameEn) {
    let lang = parseInt(localStorage.language);
    switch (lang) {
        case 1:
            return nameRu;
        case 2:
            return nameKz;
        case 3:
            return nameEn;
        default:
            return ""
    }
}

function clearEdsFields() {
    document.getElementById('subjectCn').value = '';
    document.getElementById('subjectDn').value = '';
    document.getElementById('notafter').value = '';
    document.getElementById('notbefore').value = '';
    document.getElementById('edsUsed').value = false;
}

function loginWithoutEds() {
    var user = JSON.stringify({
        login: isFieldExist("login_input") ? document.getElementById("login_input").value : null,
        iin: isFieldExist("iin_input") ? document.getElementById("iin_input").value : null,
        icNumber: isFieldExist("iin_input") ? document.getElementById("iin_input").value : isFieldExist("icNumber") ? document.getElementById("icNumber").value : null,
        password: document.getElementById("pass_input").value,
        authForDeductedStudentsAndGraduates: localStorage.authForDeductedStudentsAndGraduates
    });

    $.ajax({
        url: 'rest/api/login',
        contentType: 'application/json; charset=UTF-8',
        method: 'POST',
        beforeSend: function(request) {
            request.setRequestHeader("language", localStorage.language ? localStorage.language : 0);
        },
        dataType: 'json',
        data: user,
        error: function (error) {
            console.log("AJAX error in request: " + JSON.stringify(error, null, 2));
            blockUIStop();
            if(error.responseJSON && error.responseJSON.message){
                ToastMessage.error(error.responseJSON.message);
            }

            // $('form').submit();
        },
        success: function (response) {
            var login_status = response.login_status;
            if (login_status == 'success') {
                localStorage.token = response.auth_token;
                localStorage.uid = response.uid;
                localStorage.sid = response.sid;
                document.location.href = 'login' + window.location.search;
                // $('form').submit();
            }
        }
    });
}
function doOnLoad() {
    if (document.getElementById('login_input')) {
        document.getElementById('login_input').focus();
    } else if (document.getElementById('iin_input')) {
        document.getElementById('iin_input').focus();
    }
    initLoginType();
    let isAdminPage = window.location.pathname.includes("/admin");
    let language = 1;

    if (!isAdminPage) {
        language = localStorage.getItem("language");
        const pltLang = localStorage.getItem('pltLang');
        language = +pltLang;


        if (!language) {
            $.ajax({
                url: 'rest/api/default_auth_language',
                contentType: 'application/json; charset=UTF-8',
                method: 'GET',
                dataType: 'json',
                success: function(response) {
                    language = response.value || 1;
                    setLanguage(language);
                },
                error: function(error) {
                    console.log("Error fetching default language:", error);
                    setLanguage(1);
                }
            });
        }

        $.ajax({
            url: 'rest/api/version',
            contentType: 'application/json; charset=UTF-8',
            method: 'GET',
            dataType: 'json',
            error: function (error) {
                console.log(error);
            },
            success: function (response) {
                console.log(response);
                document.getElementById("productName").innerHTML = response.productName;
                document.getElementById("developerLink").innerHTML = '<a href="http://' + response.developerLink + '" target="_blank">' + response.developerName + '</a>';
                document.getElementById("year").innerHTML = response.year;
                document.getElementById("VERSION").innerHTML = response.VERSION;
                document.getElementById("BUILD_NUMBER").innerHTML = response.BUILD_NUMBER;
            }
        });
    }

    if (localStorage.token)
        $.ajax({
            url: 'rest/api/logout/',
            contentType: 'application/json',
            method: 'POST',
            dataType: 'json',
            headers: {
                "token": localStorage.token
            }
        });

    const pltLang = localStorage.getItem('pltLang');
    if (pltLang) {
        language = +pltLang;
    }

    localStorage.clear();
    sessionStorage.clear();
    setLanguage(language);

    $('input').on('keyup', function (e) {
        if (e.which == 13) {
            onSubmit();
        }
    });
}

function setPltLang(langCode) {
    if (langCode === 'ru') {
        return 1;
    } else if (langCode === 'kz') {
        return 2;
    } else {
        return 3;
    }
}

function setLanguage(language) {
    var languageSelect = document.getElementById("language");
    if (languageSelect) {
        languageSelect.value = language;
    }
    translate(language);
}

function getLoginType(type) {
    document.getElementById('loginRadio').value = type;
    if(type == 1) {
        document.getElementById("iin_type").style.display = "none";
        document.getElementById("login_type").style.display = "";
    } else {
        document.getElementById("login_type").style.display = "none";
        document.getElementById("iin_type").style.display = "";
    }
}

function initLoginType() {
    if(document.getElementById('loginRadio')) {
        document.getElementById('loginRadio').value = '1';
        document.getElementById('loginRadio').value.checked;
        document.getElementById("iin_type").style.display = "none";
        document.getElementById("login_type").style.display = "";
    }
}

function translate(language) {
    localStorage.language = language;
    let authenticationTabName = '';

    const loginLogoWrap = document.getElementById('loginLogoImg');
    const logoImg = document.createElement('img');
    logoImg.setAttribute('id', 'logoImg');
    function loadLogoImg() {
        if (loginLogoWrap) {
            if (!loginLogoWrap.contains(document.getElementById('logoImg'))) {
                if (loginLogoWrap) {
                    loginLogoWrap.style.maxHeight = '150px';
                    loginLogoWrap.style.marginBottom = '20px';
                    loginLogoWrap.appendChild(logoImg);
                }

                if (logoImg) {
                    fetch(`/rest/login-page/get-logo`)
                        .then(response => response.text())
                        .then(result => {
                            if (result) {
                                logoImg.src = 'data:image/PNG;base64,'+ result;
                            }
                        });
                    fetch('/rest/login-page/get-logo-location')
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Ошибка при получении позиции логотипа');
                            }
                            return response.text();
                        })
                        .then(position => {
                            switch (parseInt(position)) {
                                case 1:
                                    loginLogoWrap.style.textAlign = 'left';
                                    break;
                                case 2:
                                    loginLogoWrap.style.textAlign = 'right';
                                    break;
                                case 3:
                                    loginLogoWrap.style.textAlign = 'center';
                                    break;
                                default:
                                    loginLogoWrap.style.textAlign = 'left';
                            }
                        })
                        .catch(error => {
                            console.error('Ошибка при загрузке позиции логотипа:', error);
                            loginLogoWrap.style.textAlign = 'left';
                        });

                }
            }
        }
    }
    loadLogoImg();

    if (language == 1) {
        if (document.getElementById('login_header')) {
            document.getElementById('login_header').innerText = 'Войти в личный кабинет';
        }
        if (document.getElementById('specialButton')) {
            document.getElementById('specialButton').innerText = 'Перейти в режим для слабовидящих';
        }
        if (document.getElementById('authorization_for_expelled_and_graduates')) {
            document.getElementById('authorization_for_expelled_and_graduates').innerText = 'Авторизация для отчисленных и выпускников';
        }
        if (document.getElementById('authForDeductedStudentsAndGraduatesLabel')) {
            document.getElementById('authForDeductedStudentsAndGraduatesLabel').innerText = 'Авторизация для отчисленных и выпускников';
        }
        if (document.getElementById('forgot_your_password')) {
            document.getElementById('forgot_your_password').innerText = 'Забыли пароль?';
        }
        if (document.getElementById('login_input')) {
            document.getElementsByName('login')[0].placeholder = 'Логин';
            authenticationTabName = 'Логин и пароль';
        }
        if (document.getElementById('iin_input')) {
            document.getElementsByName('iin')[0] != undefined ? document.getElementsByName('iin')[0].placeholder = 'ИИН' : "";
            authenticationTabName = 'ИИН и пароль';
        }
        if (isFieldExist('login_input') && isFieldExist('iin_input')) {
            authenticationTabName = 'Логин, ИИН и пароль';
        }
        if (document.getElementById('login_label')) {
            document.getElementById('login_label').innerText = 'Логин';
        }
        if (document.getElementById('iin_label')) {
            document.getElementById('iin_label').innerText = 'ИИН';
        }
        if (document.getElementById('password_label')) {
            document.getElementById('password_label').innerText = 'Пароль';
        }
        if (document.getElementById('login_divider_text')) {
            document.getElementById('login_divider_text').innerText = 'Дополнительно';
        }
        document.getElementsByName('password')[0].placeholder = 'Пароль';
        document.getElementsByName('Submit1')[0].innerHTML = 'Войти';

        if (document.getElementById('applicant_registration') != null) {
            document.getElementById('applicant_registration').innerHTML = '<a style=\'text-align:center;display:block;\' href=\'registration.html\'>Регистрация абитуриентов</a>';
        }

        if (document.getElementById('edsTab') != null) {
            document.getElementById('authenticationTab').innerHTML = authenticationTabName;
            document.getElementById('edsTab').innerHTML = 'Вход по ЭЦП';
            document.getElementById('chooseCertificate').value = 'Выбрать сертификат';
        }
        if (document.getElementById('install-mobile-title') != null) {
            document.getElementById('install-mobile-title').innerText = 'Установите мобильное приложение';
        }
        if (document.getElementById('move_from_another_university') != null) {
            document.getElementById('move_from_another_university').innerHTML = '<a style=\'text-align:center;display:block;\' href=\'/v7/#/transfer-from-another-university\'>Перевод из другого ВУЗа</a>';
        }
    } else if (language == 2) {
        if (document.getElementById('login_header')) {
            document.getElementById('login_header').innerText = 'Жеке кабинетке кіру';
        }
        if (document.getElementById('specialButton')) {
            document.getElementById('specialButton').innerText = 'Көру қабілеті нашар адамдарға арналған режимге ауысу';
        }
        if (document.getElementById('authorization_for_expelled_and_graduates')) {
            document.getElementById('authorization_for_expelled_and_graduates').innerText = 'Оқудан шығарылғандарға және түлектерге арналған авторизация';
        }
        if (document.getElementById('authForDeductedStudentsAndGraduatesLabel')) {
            document.getElementById('authForDeductedStudentsAndGraduatesLabel').innerText = 'Оқудан шығарылғандарға және түлектерге арналған авторизация';
        }
        if (document.getElementById('forgot_your_password')) {
            document.getElementById('forgot_your_password').innerText = 'Құпия сөзіңізді ұмыттыңыз ба?';
        }
        if (document.getElementById('login_input')) {
            document.getElementsByName('login')[0].placeholder = 'Логин';
            authenticationTabName = 'Логин және құпия сөз';
        }
        if (document.getElementById('iin_input')) {
            document.getElementsByName('iin')[0] != undefined ? document.getElementsByName('iin')[0].placeholder = 'ЖСН' : "";
            authenticationTabName = 'ЖСН және құпия сөз';
        }
        if (isFieldExist('login_input') && isFieldExist('iin_input')) {
            authenticationTabName = 'Логин, ЖСН және құпия сөз';
        }
        if (document.getElementById('login_label')) {
            document.getElementById('login_label').innerText = 'Логин';
        }
        if (document.getElementById('iin_label')) {
            document.getElementById('iin_label').innerText = 'ЖСН';
        }
        if (document.getElementById('password_label')) {
            document.getElementById('password_label').innerText = 'Құпия сөз';
        }
        if (document.getElementById('login_divider_text')) {
            document.getElementById('login_divider_text').innerText = 'Қосымша';
        }
        document.getElementsByName('password')[0].placeholder = 'Құпия сөз';
        document.getElementsByName('Submit1')[0].innerHTML = 'Кіру';

        if (document.getElementById('applicant_registration') != null) {
            document.getElementById('applicant_registration').innerHTML = '<a style=\'text-align:center;display:block;\' href=\'registration.html\'>Талапкерлерді тіркеу</a>';
        }

        if (document.getElementById('edsTab') != null) {
            document.getElementById('authenticationTab').innerHTML = authenticationTabName;
            document.getElementById('edsTab').innerHTML = 'ЭЦҚ бойынша кіру';
            document.getElementById('chooseCertificate').value = 'Сертификатты таңдау';
        }

        if (document.getElementById('install-mobile-title') != null) {
            document.getElementById('install-mobile-title').innerText = 'Мобильді қосымшаны орнатыңыз';
        }

        if (document.getElementById('move_from_another_university') != null) {
            document.getElementById('move_from_another_university').innerText = '56789';
        }

        if (document.getElementById('move_from_another_university') != null) {
            document.getElementById('move_from_another_university').innerHTML = '<a style=\'text-align:center;display:block;\' href=\'/v7/#/transfer-from-another-university\'>Басқа ЖОО-дан ауысу</a>';
        }
    } else {
        if (document.getElementById('login_header')) {
            document.getElementById('login_header').innerText = 'Enter your personal account';
        }
        if (document.getElementById('specialButton')) {
            document.getElementById('specialButton').innerText = 'Switch to visually impaired mode';
        }
        if (document.getElementById('authorization_for_expelled_and_graduates')) {
            document.getElementById('authorization_for_expelled_and_graduates').innerText = 'Authorization for expelled and graduates';
        }
        if (document.getElementById('authForDeductedStudentsAndGraduatesLabel')) {
            document.getElementById('authForDeductedStudentsAndGraduatesLabel').innerText = 'Authorization for expelled and graduates';
        }
        if (document.getElementById('forgot_your_password')) {
            document.getElementById('forgot_your_password').innerText = 'Forgot your password?';
        }
        if (document.getElementById('login_input')) {
            document.getElementsByName('login')[0].placeholder = 'Login';
            authenticationTabName = 'Login and password';
        }
        if (document.getElementById('iin_input')) {
            document.getElementsByName('iin')[0] != undefined ? document.getElementsByName('iin')[0].placeholder = 'IIN' : "";
            authenticationTabName = 'INN and password';
        }
        if (isFieldExist('login_input') && isFieldExist('iin_input')) {
            authenticationTabName = 'Login, INN and password';
        }
        if (document.getElementById('login_label')) {
            document.getElementById('login_label').innerText = 'Login';
        }
        if (document.getElementById('iin_label')) {
            document.getElementById('iin_label').innerText = 'INN';
        }

        if (document.getElementById('password_label')) {
            document.getElementById('password_label').innerText = 'Password';
        }
        if (document.getElementById('login_divider_text')) {
            document.getElementById('login_divider_text').innerText = 'Extra';
        }
        document.getElementsByName('password')[0].placeholder = 'Password';
        document.getElementsByName('Submit1')[0].innerHTML = 'Enter';

        if (document.getElementById('applicant_registration') != null) {
            document.getElementById('applicant_registration').innerHTML = '<a style=\'text-align:center;display:block;\' href=\'registration.html\'>Applicant registration</a>';
        }

        if (document.getElementById('edsTab') != null) {
            document.getElementById('authenticationTab').innerHTML = authenticationTabName;
            document.getElementById('edsTab').innerHTML = 'Log in by EDS';
            document.getElementById('chooseCertificate').value = 'Choose the certificate';
        }

        if (document.getElementById('install-mobile-title') != null) {
            document.getElementById('install-mobile-title').innerText = 'Install the mobile application';
        }

        if (document.getElementById('move_from_another_university') != null) {
            document.getElementById('move_from_another_university').innerHTML = '<a style=\'text-align:center;display:block;\' href=\'/v7/#/transfer-from-another-university\'>Transfer from other university</a>';
        }
    }
}
function onLanguageSelect() {
    var language = document.getElementById("language").value;
    var $forgot = $("#forgot_your_password");
    if ($forgot && $forgot.length) {
        var href = $forgot.attr("href") || "";
        var base = href.split("?")[0];
        $forgot.attr("href", base + "?language=" + language);
    }
    translate(language);
}

function addNcalayerFile() {
    const js1 = document.createElement("script");
    js1.type = "text/javascript";
    js1.src = "/jscripts/ncalayer/ncalayer.js";

    const js2 = document.createElement("script");
    js2.type = "text/javascript";
    js2.onload = function() {
        setTimeout(function (){
            signXmlWithKeyTypeCall()
        },500);
    };
    js2.src = "/jscripts/ncalayer/process-ncalayer-calls.js";

    document.getElementsByTagName('head')[0].appendChild(js1);
    document.getElementsByTagName('head')[0].appendChild(js2);
}

function chooseCertificate() {
    addNcalayerFile();
    document.getElementById('edsUsed').value = true;

    var submitted = false;

    var interval = setInterval(function () {
        if (document.getElementById('signedXml').value != null && document.getElementById('signedXml').value != '') {
            onSubmit();
            submitted = true
        }
        if (submitted) {
            document.getElementById('signedXml').value = '';
            clearInterval(interval)
        }
    }, 500);
}

function viewPassword() {
    var passwordInput = document.getElementById('pass_input');
    var passStatus = document.getElementById('pass-status');

    if (passwordInput.type === 'password'){
        passwordInput.type='text';
        passStatus.className='bx bx-hide';
    } else {
        passwordInput.type='password';
        passStatus.className='bx bx-show-alt';
    }
}
