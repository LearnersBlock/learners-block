<?php
namespace IFM_Extensions;

/**
 * IFM Extensions Loader
 * 
 * Load all custom extensions for the IFM Filemanager
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

class IFM_Extensions {
    function __construct() {
        // Prepare settings
        define('LB_IFM_ROOT_PATH', dirname(dirname(__FILE__)));
        define('LB_IFM_EXTENSIONS_PATH', LB_IFM_ROOT_PATH . '/extensions');
        define('LB_API_BASE_URL', 'http://172.17.0.1:9090');

        // Load composer
        require_once LB_IFM_ROOT_PATH . '/vendor/autoload.php';

        // Load custom extensions
        $this->load_extensions();
    }


    
    /**
     * Load Extensions
     * 
     * Loads all custom extensions for the IFM Filemanager such as auth, etc.
    */

    private function load_extensions () {
        // Auth
        require_once LB_IFM_EXTENSIONS_PATH . '/auth.php';
        $extension_auth = new \IFM_Extensions\JWTAuth();

        // Lang
        require_once LB_IFM_EXTENSIONS_PATH . '/lang.php';
        $extension_lang = new \IFM_Extensions\Lang();
    }
}

new IFM_Extensions();