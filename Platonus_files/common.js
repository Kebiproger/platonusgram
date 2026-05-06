function trim(str) {
    var pos = 0;
    while (pos < str.length && str.charAt(pos) == " ") {
        str = str.substr(1, str.length);
    }
    pos = str.length - 1;
    while (pos >= 0 && pos < str.length && str.charAt(pos) == " ") {
        str = str.substr(0, str.length - 1);
        pos = str.length - 1;
    }
    return str;
}

function isIntegerNumber(str) {
    var pattern = "1234567890";
    for (var i = 0; i < str.length; i++) {
        var pos = 0;

        for (var j = 0; j < pattern.length; j++) {
            //alert(str.substr(i, 1)+" = "+pattern.substr(j, 1));
            if (str.substr(i, 1) == pattern.substr(j, 1)) {
                pos = 1;
                break;
            }
        }
        if (pos == 0)
            return false;
    }
    if (str.length > 1 && str.substr(0, 1) == "0")
        return false;
    return true;
}


function isIntegerNumber1(str) {
    var pattern = "1234567890";
    for (var i = 0; i < str.length; i++) {
        var pos = 0;

        for (var j = 0; j < pattern.length; j++) {
            if (str.substr(i, 1) == pattern.substr(j, 1)) {
                pos = 1;
                break;
            }
        }
        if (pos == 0)
            return false;
    }
    return true;
}

function isDoubleNumber(str) {

    var pattern = "1234567890.";
    var pointCount = 0;
    for (var i = 0; i < str.length; i++) {
        var pos = 0;
        for (var j = 0; j < pattern.length; j++) {
            if (str.substr(i, 1) == pattern.substr(j, 1)) {
                pos = 1;
                break;
            }
        }
        if (pos == 0)
            return false;
        if (str.substr(i, 1) == ".")
            pointCount++;
    }
    if (str.substr(0, 1) == "." || str.substr(str.length - 1, 1) == ".")
        return false;
    if (pointCount > 1)
        return false;
    return true;
}

function isDataCorrect(y, m, d) {
    if ((m == 1 || m == 3 || m == 5 || m == 7 || m == 8 || m == 10 || m == 12) && d >= 1 && d <= 31) {
        return true;
    }
    if ((m == 4 || m == 6 || m == 9 || m == 11) && d >= 1 && d <= 30) {
        return true;
    }
    if (m == 2) {
        if (y % 4 == 0) {
            if (d >= 1 && d <= 28)
                return true;
        } else {
            if (d >= 1 && d <= 29)
                return true;
        }
    }
    return false;
}

/**
 * Method return numeric value (integer or double) of a string
 * @param str - some string value
 */
function getNumberValue(str) {
    return str * 1;
}

function inserOption(selID, opt) {
    if (navigator.appName.toLowerCase().indexOf("microsoft") >= 0) {
        document.getElementById(selID).add(opt);
    } else {
        document.getElementById(selID).appendChild(opt);
    }
}


function readCookie(name) {
    var nameSG = name + "=";
    var nuller = '';
    if (document.cookie.indexOf(nameSG) == -1) {
        return nuller;
    }
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameSG) == 0) {
            return c.substring(nameSG.length, c.length);
        }
    }
    return null;
}

function newCookie(name, value, days) {
    if (days == 0) {
        var days = 360;
    }
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    } else {
        var expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function eraseCookie(name) {
    newCookie(name, "", -1);
}

function centeropen(url, winwidth, winheight) {
    var centerwin = window.open(url, "", "toolbar=1, resize=1, scrollbars=1, status=1");

    centerwin.resizeTo(winwidth, winheight)
    centerwin.moveTo(screen.width / 2 - winwidth / 2, screen.height / 2 - winheight / 2)
}


function blockUIStart(message) {
    try{
        $.blockUI({
            message: message ? message : 'Пожалуйста, подождите. Идёт обработка данных',
            css: {
                border: 'none',
                padding: '15px',
                backgroundColor: '#000',
                '-webkit-border-radius': '10px',
                '-moz-border-radius': '10px',
                opacity: 0.5,
                color: '#fff'
            }
        });
    } catch (e) {

    }
}

function blockUIStop() {
    try{
        $.unblockUI();
    } catch (e) {

    }
}
// required
// required-double
// required-int

var commonFunc = {};

commonFunc.convertToJSDate = function (date) {
    if (date == null || date == "") {
        return "";
    }
    return new Date(Date.UTC(date.year, date.month - 1, date.day))
    //return '' + commonFunc.twoFormat(date.day) + '-' + commonFunc.twoFormat(date.month) + '-' + date.year;
};

// function is used to convert date which was created by splitting date '-' in function convertToArtaDate -> ( var dateArr = date.split('-');)
commonFunc.convertToJSDateWithoutMinusMonthValue = function (date) {
    if (date == null || date == "") {
        return "";
    }
    return new Date(date.year, date.month, date.day)
    //return '' + commonFunc.twoFormat(date.day) + '-' + commonFunc.twoFormat(date.month) + '-' + date.year;
};

commonFunc.convertToArtaDate = function (date) {
    if (date == null || date === "") {
        return null;
    }
    if (date instanceof Date) {
        var year = date.getFullYear() ? date.getFullYear() : date.getYear() + 1900;
        return {year: year, month: (date.getMonth() + 1), day: date.getDate()};
    }

    // TODO: check date format
    if (moment(date, 'DD-MM-YYYY',true).isValid()) {
        var dateArr = date.split('-');
         return {year: parseInt(dateArr[2]), month: parseInt(dateArr[1]), day: parseInt(dateArr[0])};
    }
};

commonFunc.convertToDDMMYYYY = function (date) {
    if (date == null || date == "") {
        return null;
    }
    if (date instanceof Date) {
        var year = date.getFullYear ? date.getFullYear() : date.getYear() + 1900;
        return commonFunc.twoFormat(date.getDate()) + '-' + (commonFunc.twoFormat(date.getMonth() + 1)) + '-' + year;
    }
    return null;
};

commonFunc.convertToFormatDDMMYYYY = function (date) {
    if (date == null || date == "") {
        return null;
    }
    if (date instanceof Date) {
        var year = date.getFullYear ? date.getFullYear() : date.getYear() + 1900;
        return commonFunc.twoFormat(date.getDate()) + '.' + (commonFunc.twoFormat(date.getMonth() + 1)) + '.' + year;
    }
    return null;
};

commonFunc.convertToJSDateDefault = function (date, defaultDate) {
    return commonFunc.convertToJSDate(date == undefined ? defaultDate : date);
};

commonFunc.getDateByFormat = function (date, format) {
    if (date == null || date == "") {
        return null;
    }

    let jsDate = new Date(date.year, commonFunc.twoFormat(date.month) - 1, commonFunc.twoFormat(date.day), commonFunc.twoFormat(date.hour), commonFunc.twoFormat(date.minute));

    return moment(jsDate).format(format)
};

commonFunc.twoFormat = function (i) {
    if (i < 10) return '0' + i;
    return i;
};

commonFunc.txtBoxValidate = function (obj) {
    if (obj.value.length > 0) {
        $(obj).removeClass('invalid-control');
    } else {
        $(obj).addClass('invalid-control')
    }
};

commonFunc.checkDate = function (dateStr) {
    if (dateStr == null) {
        return false;
    }
    if (dateStr.split("-").length != 3) {
        return false;
    }
    if (dateStr.split("-")[0].length != 2 || dateStr.split("-")[1].length != 2 || dateStr.split("-")[2].length != 4) {
        return false;
    }

    return true;
};
commonFunc.Required = function () {
    $('.required').each(function () {
        $(this).change(function () {
            if (this.value.length > 0) {
                $(this).removeClass('invalid-control');
            } else {
                $(this).addClass('invalid-control')
            }
        })

    });
};
commonFunc.RequiredDouble = function () {
    $('.required-double').each(function () {
        $(this).change(function () {
            if (this.value.length > 0 && isDoubleNumber(this.value)) {
                $(this).removeClass('invalid-control');
            } else {
                $(this).addClass('invalid-control')
            }
        });
    });
};
commonFunc.RequiredInt = function () {
    $('.required-int').each(function () {
        $(this).change(function () {
            if (this.value.length > 0 && isIntegerNumber(this.value)) {
                $(this).removeClass('invalid-control');
            } else {
                $(this).addClass('invalid-control')
            }
        });
    });
};
commonFunc.isValid = function () {
    if ($('.invalid-control').length > 0) {
        $('.invalid-control')[0].focus();
        return false;
    }
    return true;
};
commonFunc.scrollTop = function () {
    document.body.scrollTop = document.documentElement.scrollTop = 0;
};
commonFunc.getMonthList = function (rootScope) {
    var months = [];
    if (rootScope != undefined) {
        months.push({ID: 1, name: rootScope.msgs('January')});
        months.push({ID: 2, name: rootScope.msgs('February')});
        months.push({ID: 3, name: rootScope.msgs('March')});
        months.push({ID: 4, name: rootScope.msgs('April')});
        months.push({ID: 5, name: rootScope.msgs('May')});
        months.push({ID: 6, name: rootScope.msgs('June')});
        months.push({ID: 7, name: rootScope.msgs('July')});
        months.push({ID: 8, name: rootScope.msgs('August')});
        months.push({ID: 9, name: rootScope.msgs('September')});
        months.push({ID: 10, name: rootScope.msgs('October')});
        months.push({ID: 11, name: rootScope.msgs('November')});
        months.push({ID: 12, name: rootScope.msgs('December')});
    }
    return months;
};
commonFunc.getCurrentMonthDaysCount = function (year, month) {
    if (month == 2) {
        if (year % 4 == 0)
            return 29;
        else
            return 28;
    } else if (month == 4 || month == 6 || month == 9 || month == 11) {
        return 30;
    }
    return 31;
};
commonFunc.zeroOrValue = function (value) {
    if (value) {
        return value;
    } else {
        return 0;
    }
};
commonFunc.listToIds = function (list, separator) {
    var values = [];

    if (list == null || list.length == 0) {
        return values;
    }

    angular.forEach(list, function (item) {
        values.push(item[separator]);
    });
    return values;
};

var PltMessage = (function () {
    return {
        showSuccess: showSuccess,
        showWarning: showWarning,
        showError: showError,
        showErrorWithReasons: showErrorWithReasons,
        showInfo: showInfo
    };

    function _showMsg(header, msg, messageType, reasons) {
        return {
            messageHeader: header,
            message: msg,
            messageType: messageType,
            reasons: reasons
        };
    }
    function showSuccess(header, msg) {
        return _showMsg(header, msg, enums.MessageTypes.SUCCESS_MESSAGE);
    }
    function showWarning(header, msg) {
        return _showMsg(header, msg, enums.MessageTypes.WARNING_MESSAGE);
    }
    function showError(header, msg) {
        return _showMsg(header, msg, enums.MessageTypes.ERROR_MESSAGE);
    }
    function showErrorWithReasons(header, msg, reasons) {
        return _showMsg(header, msg, enums.MessageTypes.ERROR_MESSAGE, reasons);
    }
    function showInfo(header, msg) {
        return _showMsg(header, msg, enums.MessageTypes.INFORMATION_MESSAGE);
    }
})();

const ToastMessage = (function () {
    return {
        showPltMessage: showPltMessage,
        success: _success,
        error: _error,
        warning: _warning,
        info: _info
    };

    function showPltMessage(message, override) {
        if (message.messageType == enums.MessageTypes.SUCCESS_MESSAGE) {
            _success(message.message, message.messageHeader, override);
            if (message.reasons) {
                for (const reason of message.reasons) {
                    _success(reason, null, override);
                }
            }
        } else if (message.messageType == enums.MessageTypes.ERROR_MESSAGE) {
            _error(message.message, message.messageHeader);
            if (message.reasons) {
                for (const reason of message.reasons) {
                    _error(reason, null, override);
                }
            }
        } else if (message.messageType == enums.MessageTypes.WARNING_MESSAGE) {
            _warning(message.message, message.messageHeader);
            if (message.reasons) {
                for (const reason of message.reasons) {
                    _warning(reason, null, override);
                }
            }
        } else {
            if (message.message || message.messageHeader) {
                _info(message.message, message.messageHeader);
            }
            if (message.reasons) {
                for (const reason of message.reasons) {
                    _info(reason, null, override);
                }
            }
        }
    }

    function _success(text, header, override) {
        toastr.success(text, header, override);
    }

    function _error(text, header, override) {
        toastr.error(text, header, override);
    }

    function _warning(text, header, override) {
        toastr.warning(text, header, override);
    }

    function _info(text, header, override) {
        toastr.info(text, header, override);
    }
})();


var PltLanguageModule = (function () {
    return {
        getLanguageID: getLanguageID,
        getLanguage: getLanguage,
        getLocalizedByID: getLocalizedByID,
        getLocalized: getLocalized
    };

    function getLanguageID(language) {
        if (language == "ru") return 1;
        else if (language == "kz") return 2;
        else if (language == "en") return 3;
        return 1;
    }

    function getLanguage(languageID) {
        if (languageID == 1) return "ru";
        else if (languageID == 2) return "kz";
        else if (languageID == 3) return "en";
        return "ru";
    }

    function getLocalizedByID(languageID, kz, ru, en) {
        if (languageID == 1) return ru;
        else if (languageID == 2) return kz;
        else if (languageID == 3) return en;
        return ru;
    }

    function getLocalized(language, kz, ru, en) {
        return getLocalizedByID(getLanguageID(language), kz, ru, en);
    }
})();

var PltArrayModule = (function () {
    var moveToBeginning = function (array, propertyName, id) {
        var element = removeElement(array, propertyName, id);
        if (element) {
            array.unshift(element);
        }
    };
    var moveToEnding = function (array, propertyName, id) {
        var element = removeElement(array, propertyName, id);
        if (element) {
            array.push(element);
        }
    };
    var removeElement = function (array, propertyName, id) {
        for (var index = 0; index < array.length; index++) {
            if (array[index][propertyName] == id) {
                var element = array[index];
                array.splice(index, 1);
                return element;
            }
        }
        return null;
    };

    return {
        moveToBeginning: moveToBeginning,
        moveToEnding: moveToEnding,
        removeElement: removeElement
    };
})();

var PltNumberModule = (function () {
    return {
        roundWithPrecision: roundWithPrecision,
        inRange: inRange
    };

    function roundWithPrecision(number, power) {
        var n = Math.pow(10, power);
        return Math.round(number * n) / n;
    }

    function inRange(number, start, end) {
        return number >= start && number <= end;
    }
})();

var PltValidationModule = (function () {
    var isNumber = function (str) {
        var pattern = /^\d+$/; // Matches any decimal digit. Equivalent to [0-9]
        return pattern.test(str);
    };
    var isEmpty = function (str) {
        if (str == undefined || str == null) {
            return true;
        } else {
            var pattern = /\S+/; // match any non-white space character [^\r\n\t\f ]
            return !pattern.test(str);
        }
    };
    var isIIN = function (str) {
        var pattern = /^\d{12}$/; // Matches any decimal digit with length 12
        return pattern.test(str);
    };
    var isEmail = function (str) {
        var pattern = /^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
        return pattern.test(str);
    };

    return {
        isNumber: isNumber,
        isEmpty: isEmpty,
        isIIN: isIIN,
        isEmail: isEmail
    };
})();

var PltMsgsModule = (function () {
    return {
        missingValue: missingValue,
        wrongValue: wrongValue,
        notAllFieldsWereSelected: notAllFieldsWereSelected,
        notChecked: notChecked,
        notSelected: notSelected
    };
    function missingValue(msgs, str, doNotTranslate) {
        return msgs('Missing value in the field') + ' - ' + _getMessage(msgs, str, doNotTranslate);
    }

    function wrongValue(msgs, str, doNotTranslate) {
        return msgs('Wrong value in the field') + ' - ' + _getMessage(msgs, str, doNotTranslate);
    }

    function notAllFieldsWereSelected(msgs, str, doNotTranslate) {
        return msgs('Not all fields were selected') + ' - ' + _getMessage(msgs, str, doNotTranslate);
    }

    function notChecked(msgs, str, doNotTranslate) {
        return msgs('You did not select the field') + ' - ' + _getMessage(msgs, str, doNotTranslate);
    }


    function notSelected(msgs, str, doNotTranslate) {
        return msgs('The corresponding value is not selected in the tab') + ' - ' + _getMessage(msgs, str, doNotTranslate);
    }

    /* pass doNotTranslate == true, to returns message as passed, without translating.
     Otherwise method translates message according to locale */
    function _getMessage(msgs, str, doNotTranslate) {
        return doNotTranslate ? str : msgs(str);
    }
})();

var PltDateModule = (function () {
    return {
        dayDifference: dayDifference,
        toArtaThenToJs: toArtaThenToJs,
        addYears: addYears,
        parseDate: parseDate,
        parse: parse,
        isAdult: isAdult,
        format_DD_MM_YYYY: format_DD_MM_YYYY
    };

    function toArtaThenToJs(dateStr) {
        return commonFunc.convertToJSDate(commonFunc.convertToArtaDate(dateStr));
    }

    function addYears(date, years) {
        date.setFullYear(date.getFullYear() + years);
    }

    function dayDifference(startDate, endDate) {
        return Math.floor(Math.abs(endDate - startDate) / (1000 * 60 * 60 * 24));
    }

    /** date format should be dd-MM-yyyy */
    function parseDate(date) {
        return date.split("-");
    }

    /** date format should be dd-MM-yyyy */
    function parse(value) {
        var args = value.split("-");
        var date = new Date(parseInt(args[2]), parseInt(args[1]) - 1, parseInt(args[0]));
        date.setHours(0, 0, 0, 0);
        return date;
    }

    function format_DD_MM_YYYY(date) {
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();
        return `${day < 10 ? '0' + day : day}-${month < 10 ? '0' + month : month}-${year}`;
    }

    /** birthDate format should be dd-MM-yyyy */
    function isAdult(birthDate) {
        if (!commonFunc.checkDate(birthDate)) return false;

        let args = parseDate(birthDate);
        let birthdayDay = parseInt(args[0]);
        let birthdayMonth = parseInt(args[1]);
        let birthdayYear = parseInt(args[2]);

        let now = new Date();
        let year = now.getFullYear() - birthdayYear;

        if (year > 18) {
            return true;
        } else if (year === 18) {
            let month = (now.getMonth() + 1) - birthdayMonth;
            if (month > 0) {
                return true;
            } else if (month === 0) {
                let day = now.getDate() - birthdayDay;
                if (day >= 0) {
                    return true;
                }
            }
        }
        return false;
    }

})();

var PltTimeModule = (function () {
    return {
        format_HH_MM: format_HH_MM,
        convert_ISO_8601: convert_ISO_8601
    };

    function format_HH_MM(day) {
        return `${day.getHours().toString().padStart(2, '0')}:${day.getMinutes().toString().padStart(2, '0')}`;
    }

    function convert_ISO_8601(value) {
        var timezoneOffsetMinutes = new Date().getTimezoneOffset();
        let times = value.split(':');

        let day = new Date();
        day.setHours(times[0]);
        day.setMinutes(times[1]);

        var date = new Date();
        date.setMilliseconds( day.getMilliseconds() - timezoneOffsetMinutes * 60 * 1000);

        return date.toISOString();
    }
})();

var PltDomManipulation = (function () {
    var toggleVisibility = function (elementID) {
        var element = document.getElementById(elementID);
        if (element.style.visibility === 'hidden') {
            element.style.visibility = 'visible';
        } else {
            element.style.visibility = 'hidden';
        }
    };
    var toggleDisplay = function (elementID) {
        var element = document.getElementById(elementID);
        if (element.style.display === 'none') {
            element.style.display = 'block';
        } else {
            element.style.display = 'none';
        }
    };

    var changeVisibility = function (isVisible, elementID) {
        var element = document.getElementById(elementID);
        element.style.visibility = isVisible ? 'visible' : 'hidden';
    };

    var changeDisplay = function (isVisible, elementID) {
        var element = document.getElementById(elementID);
        element.style.display = isVisible ? 'block' : 'none';
    };

    return {
        toggleVisibility: toggleVisibility,
        toggleDisplay: toggleDisplay,
        changeVisibility: changeVisibility,
        changeDisplay: changeDisplay
    };
})();

var PltIntModule = (function () {
    var getValue = function (value) {
        return value == null ? 0 : parseInt(value);
    };

    return {
        getValue: getValue
    };
})();

var PltObjectModule = (function () {
    var isEmpty = function (obj) {
        return obj == null || Object.keys(obj).length == 0;
    };

    var isNotEmpty = function (obj) {
        return !isEmpty(obj);
    };

    return {
        isEmpty: isEmpty,
        isNotEmpty: isNotEmpty
    };
})();

var PltCalendarDateModule = (function () {
    return {
        parseDate: parseDate
    };

    /** date format should be dd-MM-yyyy */
    function parseDate(date) {
        if (date == null || date == "") {
            return null;
        }
        return new Date(date.replace( /(\d{2})-(\d{2})-(\d{4})/, "$2/$1/$3"))
    }

})();

var PltTextModule = (function () {
    var isEmpty = function (obj) {
        return obj == null || obj.length == 0;
    };

    var isNotEmpty = function (obj) {
        return !isEmpty(obj);
    };

    return {
        isEmpty: isEmpty,
        isNotEmpty: isNotEmpty
    };
})();

var PltSimpleObjectListModule = (function () {
    var getIndex = function (list, ID) {
        if (list && list.length > 0) {
            return list.findIndex(item => item.ID === ID);
        }
        return -1;
    };

    var findByID = function (list, ID) {
        if (list && list.length > 0) {
            return list.find(item => item.ID === ID);
        }
        return null;
    };

    var addIfAbsent = function (mainList, list) {
        if (!mainList) {
            mainList = [];
        }

        angular.forEach(list, function (item) {
            var foundItem = findByID(mainList, item.ID);
            if (!foundItem) {
                mainList.push(item);
            }
        });
    };

    var deleteIfExists = function (mainList, list) {
        if (!mainList) {
            mainList = [];
        }

        if (list) {
            for(var i = list.length - 1; i >= 0; i--) {
                var foundIndex = getIndex(mainList, list[i].ID);
                if (foundIndex > -1) {
                    mainList.splice(foundIndex, 1);
                }
            }
        }
    };

    var getIdList = function (list) {
        return list.map(i => i.ID);
    };

    return {
        findByID: findByID,
        addIfAbsent: addIfAbsent,
        deleteIfExists: deleteIfExists,
        getIdList: getIdList,
    };
})();

var PltBinarySearchModule = (function () {
    var getSelectedList = function (typeList, value) {
        var selectedList = [];
        if (value < 2) {
            return selectedList;
        }

        var binStr = ((value >>> 0).toString(2)).split("").reverse().join("");
        for (i = 1; i < binStr.length; i++) {
            if (binStr.charAt(i) == '1') {
                selectedList.push(typeList[i - 1]);
            }
        }

        return selectedList;
    };

    var getSelectedValue = function (list) {
        var value = 0;

        for (i = 0; i < list.length; i++) {
            value += Math.pow(2, list[i].id);
        }

        return value;
    };

    return {
        getSelectedList: getSelectedList,
        getSelectedValue: getSelectedValue
    };
})();

var PltNgTableModule = (function () {
    var resetPageNumber = function (table, tableParams, searchParams) {
        var newParams = angular.copy(searchParams);
        delete newParams.partNumber;
        delete newParams.total;

        if (!angular.equals(newParams, table.oldParams)) {
            table.oldParams = angular.copy(newParams);
        }
    };

    return {
        resetPageNumber: resetPageNumber
    };
})();

var PltBase64Module = (function () {
    var toArrayBuffer = function (base64) {
        let binary_string = window.atob(base64);
        let len = binary_string.length;
        let bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binary_string.charCodeAt(i);
        }
        return bytes.buffer;
    };

    return {
        toArrayBuffer: toArrayBuffer
    };
})();

var PltMapModule = (function () {
    var valueOf = function (text, delimiter) {
        var map = {};

        if (!delimiter) {
            delimiter = ",";
        }

        var arr = text.split(delimiter);
        arr.forEach(function(item) {
            var args = item.split("=");
            var key = args[0];
            var value = args[1];
            map[key] = value;
        });

        return map;
    };

    return {
        valueOf: valueOf
    };
})();

var PltFileDownloader = (function () {
    var download = function (response) {
        const bytes = PltBase64Module.toArrayBuffer(response.bytes);
        const file = new Blob([bytes], {type: response.contentType});
        const fileURL = URL.createObjectURL(file);
        const a = document.createElement('a');
        a.href = fileURL;
        a.target = '_blank';
        a.download = response.fileName;
        document.body.appendChild(a);
        a.click();
    };

    return {
        download: download
    }
})();

var PltUUID = (function () {
    var S4 = function () {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }

    var generate = function () {
        return S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4();
    }

    return {
        generate: generate
    }
})();
``
const PltSwal = (function () {
    const confirmMessage = function (title, confirmButtonText, cancelButtonText, confirmButtonCustomClasses = null, cancelButtonCustomClasses = null, titleClass = 'fs-6 mw-100') {
        if (!confirmButtonCustomClasses) {
            confirmButtonCustomClasses = 'btn btn-primary me-3';
        }

        if (!cancelButtonCustomClasses) {
            cancelButtonCustomClasses = 'btn btn-label-secondary';
        }

        return Swal.fire({
            title: title,
            showCancelButton: true,
            confirmButtonText: confirmButtonText,
            cancelButtonText: cancelButtonText,
            customClass: {
                title: titleClass,
                confirmButton: confirmButtonCustomClasses,
                cancelButton: cancelButtonCustomClasses
            },
            buttonsStyling: false
        });
    };

    const errorMessage = function (title, text) {
        return Swal.fire({
            icon: 'error',
            title: title,
            text: text,
            customClass: {
                icon: 'fs-6',
                title: 'fs-5 mw-100 mt-2',
                htmlContainer: 'fs-6 mw-100',
                confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false
        });
    };

    const infoMessage = function (title, text) {
        return Swal.fire({
            icon: 'info',
            title: title,
            text: text,
            customClass: {
                icon: 'fs-6',
                title: 'fs-5 mw-100 mt-2',
                htmlContainer: 'fs-6 mw-100',
                confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false
        });
    };

    const warningMessage = function (title, text) {
        return Swal.fire({
            icon: 'warning',
            title: title,
            text: text,
            customClass: {
                icon: 'fs-6',
                title: 'fs-5 mw-100 mt-2',
                htmlContainer: 'fs-6 mw-100',
                confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false
        });
    };

    const successMessage = function (title, text) {
        return Swal.fire({
            icon: 'success',
            title: title,
            text: text,
            customClass: {
                icon: 'fs-6',
                title: 'fs-5 mw-100 mt-2',
                htmlContainer: 'fs-6 mw-100',
                confirmButton: 'btn btn-success'
            }
        });
    };

    const showPltMessage = function (message) {
        if (message.reasons && message.reasons.length > 0) {
            let result =  '';
            message.reasons.forEach(reason => {
                if (result.length > 0) {
                    result += ',';
                }
                result += reason;
            });

            message.reasons = null;
            message.message = result;
        }
        if (message.messageType == enums.MessageTypes.ERROR_MESSAGE) {
            errorMessage(message.messageHeader, message.message);
        } else if (message.messageType == enums.MessageTypes.WARNING_MESSAGE) {
            warningMessage(message.messageHeader, message.message);
        } else if (message.messageType == enums.MessageTypes.SUCCESS_MESSAGE) {
            successMessage(message.messageHeader, message.message);
        } else {
            infoMessage(message.messageHeader, message.message);
        }
    };

    return {
        confirmMessage: confirmMessage,
        errorMessage: errorMessage,
        infoMessage: infoMessage,
        warningMessage: warningMessage,
        successMessage: successMessage,
        showPltMessage: showPltMessage
    };
})();
