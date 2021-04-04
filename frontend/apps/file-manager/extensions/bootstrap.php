<?php
namespace IFM_Extensions;

/**
 * IFM Extensions Loader
 * 
 * Load all custom extensions for the IFM Filemanager
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

class IFM_Extensions {
    function __construct() {
        // Set environment vars
        $is_dev_env     = (getenv('ENV') === 'development');
        $host_dev_env   = '0.0.0.0:9090';
        $host_prod_env  = $_SERVER['HTTP_HOST'];
        
        // Prepare settings
        define('ROOT_PATH', dirname(dirname(__FILE__)));
        define('EXTENSIONS_PATH', ROOT_PATH . '/extensions');
        define('LB_API_BASE_URL', $is_dev_env ? $host_dev_env : $host_prod_env);

        // Load composer
        require_once ROOT_PATH . '/vendor/autoload.php';

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
        require_once EXTENSIONS_PATH . '/auth.php';
        $extension_auth = new \IFM_Extensions\JWTAuth();

        // Lang
        require_once EXTENSIONS_PATH . '/lang.php';
        $extension_lang = new \IFM_Extensions\Lang();
    }
}

new IFM_Extensions();