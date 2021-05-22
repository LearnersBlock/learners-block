<?php
namespace IFM_Extensions;

/**
 * Path Config Controller
 * 
 * Extension to support multiple paths to access IFM and change the public dir dynamically
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

class PathConfig extends IFM_Extensions {
    function __construct() {
        // Set config 
        $this->auth_env_var_name = 'LB_IFM_AUTHENTICATED';

        // Get current request uri
        $this->current_path = $_SERVER['REQUEST_URI'];
        
        // Load config
        $this->paths_config = array(
            '/files/'    => array(
                'auth'      => array(
                    'required'              => false,
                    'error_redirect_path'   => ''
                ),
                'config'    => array(
                    'IFM_ROOT_DIR'          => '/app/public/storage/fileshare/',
                    'IFM_ROOT_PUBLIC_URL'   => '/storage/fileshare/'
                )
            ),
            '/upload-files/'    => array(
                'auth'      => array(
                    'required'              => true,
                    'error_redirect_path'   => '/settings'
                ),
                'config'    => array(
                    'IFM_ROOT_DIR'          => '/app/public/storage',
                    'IFM_ROOT_PUBLIC_URL'   => '/storage/',
                    'IFM_API_COPYMOVE'      => '1',
                    'IFM_API_CREATEDIR'     => '1',
                    'IFM_API_DELETE'        => '1',
                    'IFM_API_EXTRACT'       => '1',
                    'IFM_API_UPLOAD'        => '1',
                    'IFM_API_REMOTEUPLOAD'  => '1',
                    'IFM_API_RENAME'        => '1'
                )
            ),
            '/upload-website/'  => array(
                'auth'      => array(
                    'required'              => true,
                    'error_redirect_path'   => '/settings'
                ),
                'config'    => array(
                    'IFM_ROOT_DIR'          => '/app/public/storage/website',
                    'IFM_ROOT_PUBLIC_URL'   => '/storage/website/',
                    'IFM_API_COPYMOVE'      => '1',
                    'IFM_API_CREATEDIR'     => '1',
                    'IFM_API_DELETE'        => '1',
                    'IFM_API_EXTRACT'       => '1',
                    'IFM_API_UPLOAD'        => '1',
                    'IFM_API_REMOTEUPLOAD'  => '1',
                    'IFM_API_RENAME'        => '1'
                )
            ),
            '/library/' => array(
                'auth'      => array(
                    'required'              => false,
                    'error_redirect_path'   => ''
                ),
                'config'    => array(
                    'IFM_ROOT_DIR'          => '/app/public/storage/library',
                    'IFM_ROOT_PUBLIC_URL'   => '/storage/library/'
                )
            )
        );

        // Start
        $this->init();
    }



    /**
     * Init
     * 
     * Searches for the current request URI in the config array to determine which configuration to load.
     * 
     * @return void.
     */

    private function init () {
        // Ensure we have a path to work with
        if (!$this->current_path || !isset($this->paths_config[$this->current_path])) {
            return false;
        }

        // If so, get the config array to process
        $config = $this->paths_config[$this->current_path];
        $config = json_decode(json_encode($config, JSON_FORCE_OBJECT));

        // Check for auth requirements
        if ($config->auth->required) {
            // Get env var stored by auth extension
            $is_authenticated = filter_var(getenv("{$this->auth_env_var_name}"), FILTER_VALIDATE_BOOLEAN);

            // If auth has not suceeded 
            if (!$is_authenticated) {
                // Validate and set redirect destination
                $redirect_to = isset($config->auth->error_redirect_path) ? trim($config->auth->error_redirect_path) : '/';
                $redirect_to = !empty($redirect_to) ? $redirect_to : '/';
                
                // Run redirect
                header("Location: {$redirect_to}");
            }
        }

        // Otherwise, if auth succeeded or wasn't required, process configuration
        $this->enable_config($config->config);
    }



    /**
     * Enable configuration
     * 
     * Processes the previously matched config object and enables it by setting the env variables read by IFM.
     * 
     * @param Array $params The config params to set.
     * @return void.
     */

    private function enable_config($params) {
        // Loop over all params
        foreach($params as $setting => $value) {
            // Inject the param as env variables
            putenv("$setting=$value");
        }
    }
}