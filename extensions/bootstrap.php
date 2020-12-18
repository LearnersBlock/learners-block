<?php
namespace IFM_Extensions;
use Dotenv;

/**
 * IFM Extensions Loader
 * 
 * Load all custom extensions for the IFM filemanager
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

class IFM_Extensions {
    function __construct() {
        // define some base constants
        define('ROOT_PATH', dirname(dirname(__FILE__)));
        define('EXTENSIONS_PATH', ROOT_PATH . '/extensions');

        // load composer
        require_once ROOT_PATH . '/vendor/autoload.php';

        // load all custom extensions
        $this->load_dotenv();
        $this->load_extensions();
    }



    /**
     * load_dotenv
     * 
     * Loads the .env confile file into the filemanager to provide environment
     * variable support for IFM and the extensions
    */

    private function load_dotenv () {
        // load dotenv config
        $dotenv = Dotenv\Dotenv::createImmutable(ROOT_PATH);
        $dotenv->load();
    }


    
    /**
     * load_extensions
     * 
     * Loads all custom extensions for the IFM filemanager such as auth, etc.
    */

    private function load_extensions () {
        // auth
        require_once EXTENSIONS_PATH . '/auth.php';
        $extension_auth = new \IFM_Extensions\JWTAuth();

        // lang
        require_once EXTENSIONS_PATH . '/lang.php';
        $extension_lang = new \IFM_Extensions\Lang();
    }
}


new IFM_Extensions();