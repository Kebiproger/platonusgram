/**
 * Config
 * -------------------------------------------------------------------------------------
 * ! IMPORTANT: Make sure you clear the browser local storage In order to see the config changes in the template.
 * ! To clear local storage: (https://www.leadshook.com/help/how-to-clear-local-storage-in-google-chrome-browser/).
 */

'use strict';

// JS global variables
let config = {
  colors: {
    primary: '#696cff',
    secondary: '#8592a3',
    success: '#71dd37',
    info: '#03c3ec',
    warning: '#ffab00',
    danger: '#ff3e1d',
    dark: '#233446',
    black: '#000',
    white: '#fff',
    body: '#f4f5fb',
    headingColor: '#566a7f',
    axisColor: '#a1acb8',
    borderColor: '#eceef1'
  },
  colors_label: {
    primary: '#666ee81a',
    secondary: '#8897aa1a',
    success: '#28d0941a',
    info: '#1e9ff21a',
    warning: '#ff91491a',
    danger: '#ff49611a',
    dark: '#181c211a'
  },
  colors_dark: {
    cardColor: '#2b2c40',
    headingColor: '#cbcbe2',
    axisColor: '#7071a4',
    borderColor: '#444564'
  },
  enableMenuLocalStorage: true // Enable menu state with local storage support
};

let assetsPath = document.documentElement.getAttribute('data-assets-path'),
  templateName = document.documentElement.getAttribute('data-template'),
  rtlSupport = false; // set true for rtl support (rtl + ltr), false for ltr only.

/**
 * TemplateCustomizer
 * ! You must use(include) template-customizer.js to use TemplateCustomizer settings
 * -----------------------------------------------------------------------------------------------
 */

// To use more themes, just push it to THEMES object.

/* TemplateCustomizer.THEMES.push({
  name: 'theme-raspberry',
  title: 'Raspberry'
}); */

/**
 * TemplateCustomizer settings
 * -------------------------------------------------------------------------------------
 * cssPath: Core CSS file path
 * themesPath: Theme CSS file path
 * displayCustomizer: true(Show customizer), false(Hide customizer)
 * lang: To set default language, Add more langues and set default. Fallback language is 'en'
 * controls: [ 'rtl','style','layoutType','showDropdownOnHover','layoutNavbarFixed','layoutFooterFixed','themes'] | Show/Hide customizer controls
 * defaultTheme: 0(Default), 1(Semi Dark), 2(Bordered)
 * defaultStyle: 'light', 'dark' (Mode)
 * defaultTextDir: 'ltr', 'rtl' (rtlSupport must be true for rtl mode)
 * defaultLayoutType: 'static', 'fixed'
 * defaultMenuCollapsed: true, false
 * defaultNavbarFixed: true, false
 * defaultFooterFixed: true, false
 * defaultShowDropdownOnHover : true, false (for horizontal layout only)
 */

if (typeof TemplateCustomizer !== 'undefined') {
  TemplateCustomizer.LANGUAGES = {
    ru: {
      "panel_header": "Настройка шаблона",
      "panel_sub_header": "Customize and preview in real time",
      "theming_header": "THEMING",
      "theme_header": "THEME",
      "theme_label": "Themes",
      "style_label": "Style (Mode)",
      "style_switch_light": "Light",
      "style_switch_dark": "Dark",
      "layout_header": "LAYOUT",
      "layout_label": "Layout (Menu)",
      "layout_static": "Static",
      "layout_offcanvas": "Offcanvas",
      "layout_fixed": "Fixed",
      "layout_fixed_offcanvas": "Fixed offcanvas",
      "layout_flipped_label": "Menu flipped",
      "layout_dd_open_label": "Dropdown on hover",
      "layout_navbar_label": "Fixed navbar",
      "layout_footer_label": "Fixed footer",
      "misc_header": "MISC",
      "rtl_label": "RTL direction"
    },
    kz: {
      "panel_header": "THEME CUSTOMIZER",
      "panel_sub_header": "Customize and preview in real time",
      "theming_header": "THEMING",
      "theme_header": "THEME",
      "theme_label": "Themes",
      "style_label": "Style (Mode)",
      "style_switch_light": "Light",
      "style_switch_dark": "Dark",
      "layout_header": "LAYOUT",
      "layout_label": "Layout (Menu)",
      "layout_static": "Static",
      "layout_offcanvas": "Offcanvas",
      "layout_fixed": "Fixed",
      "layout_fixed_offcanvas": "Fixed offcanvas",
      "layout_flipped_label": "Menu flipped",
      "layout_dd_open_label": "Dropdown on hover",
      "layout_navbar_label": "Fixed navbar",
      "layout_footer_label": "Fixed footer",
      "misc_header": "MISC",
      "rtl_label": "RTL direction"
    },
    en: {
      "panel_header": "THEME CUSTOMIZER",
      "panel_sub_header": "Customize and preview in real time",
      "theming_header": "THEMING",
      "theme_header": "THEME",
      "theme_label": "Themes",
      "style_label": "Style (Mode)",
      "style_switch_light": "Light",
      "style_switch_dark": "Dark",
      "layout_header": "LAYOUT",
      "layout_label": "Layout (Menu)",
      "layout_static": "Static",
      "layout_offcanvas": "Offcanvas",
      "layout_fixed": "Fixed",
      "layout_fixed_offcanvas": "Fixed offcanvas",
      "layout_flipped_label": "Menu flipped",
      "layout_dd_open_label": "Dropdown on hover",
      "layout_navbar_label": "Fixed navbar",
      "layout_footer_label": "Fixed footer",
      "misc_header": "MISC",
      "rtl_label": "RTL direction"
    }
  };

  window.templateCustomizer = new TemplateCustomizer({
    cssPath: assetsPath + 'css' + (rtlSupport ? '/rtl' : '') + '/',
    themesPath: assetsPath + 'css' + (rtlSupport ? '/rtl' : '') + '/',
    displayCustomizer: true,
    lang: 'ru',
    // defaultTheme: 1,
    // defaultStyle: 'light',
    // defaultTextDir: 'ltr',
    // defaultLayoutType: 'fixed',
    // defaultMenuCollapsed: false,
    // defaultNavbarFixed: true,
    // defaultFooterFixed: true,
    defaultShowDropdownOnHover: true,
    // controls: [
    //   // 'rtl',
    //   'style',
    //   // 'layoutType',
    //   // 'showDropdownOnHover',
    //   'layoutNavbarFixed',
    //   'layoutFooterFixed',
    //   'themes'
    // ],
  });
}
