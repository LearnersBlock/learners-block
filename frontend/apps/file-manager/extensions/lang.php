<?php
namespace IFM_Extensions;

/**
 * Lang Controller
 * 
 * Controller to get/set the language parameter for the filemanager
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

class Lang extends IFM_Extensions {
    function __construct() {
        // prepare variables
        $this->lang = 'en';

        // start lang logic
        $this->check_lang_param();
    }



    /**
     * check_lang_param
     * 
     * Checks whether or not the lang URL parameter was set. If so, it will
     * proceed to set the lang env variable.
    */

    private function check_lang_param () {
        if (isset($_GET['lang'])) {
            // store lang param
            $this->lang = (string) $_GET['lang'];

            // now check
            if ($this->lang) {
                $this->set_lang();
            }
        }
    }



    /**
     * set_lang
     * 
     * Sets the language envariable using the previously stored language fetched
     * from the URL parameter.
    */

    private function set_lang() {
        // inject the language param as an env variable
        putenv("IFM_LANGUAGE=$this->lang");
    }
}