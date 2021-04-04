<?php
namespace IFM_Extensions;

/**
 * Lang Controller
 * 
 * Extension to get/set the language parameter based on the cookie stored by the interface. The cookie is named 'lang'
 * and stores the prefered language as i18n locale, i.e. 'en-US' 
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

class Lang extends IFM_Extensions {
    function __construct() {
        // Set default
        $this->lang = 'en-US';

        // Start lang logic
        $this->check_lang_cookie();
    }



    /**
     * Check for lang cookie
     * 
     * Checks whether or not the lang cookie exists and if so, update the language settings.
     */

    private function check_lang_cookie () {
        // Get the language cookie
        $cookie_lang = isset($_COOKIE['lang']) ? filter_var($_COOKIE['lang'], FILTER_SANITIZE_STRING) : false;
        
        // Check if we have a value to work with
        if ($cookie_lang) {
            // If so, update the lang
            $this->lang = $cookie_lang;
        }

        // Update the Filemanager settings
        $this->set_lang();
    }



    /**
     * Set language
     * 
     * Sets the language env variable using the previously fetched cookie or fallback value.
    */

    private function set_lang() {
        // Inject the language param as an env variable
        putenv("IFM_LANGUAGE=$this->lang");
    }
}