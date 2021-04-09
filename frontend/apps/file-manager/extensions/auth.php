<?php
namespace IFM_Extensions;
use GuzzleHttp;
use GuzzleHttp\Exception\ClientException;

/**
 * Auth Controller
 * 
 * Extension to handle authentication between the interface and the file manager (i.e. for admin access)
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

class JWTAuth extends IFM_Extensions {
    function __construct() {
        // Set config
        $this->auth_cookie_name = 'access_token_cookie';

        // Set default admin params
        $this->admin_params = array(
            'IFM_ROOT_DIR'          => $_ENV['FILEMANAGER_ADMIN_ROOT_DIR'] ?: '/app/web/public/storage',
            'IFM_ROOT_PUBLIC_URL'   => $_ENV['FILEMANAGER_ADMIN_PUBLIC_URL'] ?: '/storage/',
            'IFM_API_COPYMOVE'      => '1',
            'IFM_API_CREATEDIR'     => '1',
            'IFM_API_CREATEFILE'    => '1',
            'IFM_API_EDIT'          => '1',
            'IFM_API_DELETE'        => '1',
            'IFM_API_EXTRACT'       => '1',
            'IFM_API_UPLOAD'        => '1',
            'IFM_API_REMOTEUPLOAD'  => '1',
            'IFM_API_RENAME'        => '1'
        );

        // Prepare guzzle client
        $this->client = new GuzzleHttp\Client();

        // Start authentication
        $this->is_auth_enabled();
    }



    /**
     * Check if auth mode has been enabled 
     * 
     * Checks whether or not the file manager admin mode has been enabled via the "mode=admin" URL parameter. If so, run
     * the authentication process.
     * 
     * @return void.
     */

    private function is_auth_enabled () {
        if (isset($_GET['mode'])) {
            // Store mode param
            $mode = filter_var($_GET['mode'], FILTER_SANITIZE_STRING);

            // Check for mode type
            if ($mode === 'admin') {
                $this->authenticate();
            }
        }
    }



    /**
     * Authenticate
     * 
     * Runs the authentication process by validating the token stored as cookie using the backend API. If the
     * authentication process fails, the user is redirected to the interface's loging form.
     * 
     * @return void.
     */

    private function authenticate () {
        // Get the token
        $token = (string) $this->get_token_from_cookie();

        // Check if we have a token to work with
        if ($token) {
            try {
                // Run the request
                $response = $this->client->request(
                    'GET',
                    LB_API_BASE_URL . '/v1/verifylogin',
                    [
                        'headers' => [
                            'Authorization' => 'Bearer ' . $token,
                            'Accept'        => 'application/json',
                        ]
                    ]
                );

                // Token verification was a success, process request response
                $body = $response->getBody(true);
                $body = json_decode($body);

                // Make sure we have the correct response
                if ($response->getStatusCode() == 200 && $body->logged_in) {
                    // And enable the admin mode
                    $this->enable_admin_mode();
                }
            } catch (ClientException $e) {
                // Handle client exceptions (4xx)
                $response = $e->getResponse();
                $response_code = $response->getStatusCode();
                $response_body = $response->getBody()->getContents();

                // Check status code to match the expected 401
                if (isset($response_code) && $response_code === 401) {
                    header('Location: /settings');
                }
            }
        } else {
            // Otherwise, if no token cookie present, redirect back to the settings page
            header('Location: /settings'); 
        }
    }



    /**
     * Get token
     * 
     * Fetches the JWT token from the auth cookie and returns it to the authentication method to validate it.
     * 
     * @return String|Boolean The JWT token or false if none available.
     */

    private function get_token_from_cookie () {
        if (isset($_COOKIE[$this->auth_cookie_name])) {
            // Decode the JSON string saved in the cookie
            $token = filter_var($_COOKIE[$this->auth_cookie_name], FILTER_SANITIZE_STRING);

            // Check we have a token in here
            if (isset($token)) {
                // If so, return it
                return $token;
            }
            
            // Otherwise abort
            return false;
        }

        // Abort
        return false;
    }



    /**
     * Enable admin mode
     * 
     * Adds all the env varaibles required to enable the filemanager admin mode based on the parameters and values
     * defined in the constructor above. 
     * 
     * @return void.
     */

    private function enable_admin_mode() {
        // Loop over all admin params
        foreach($this->admin_params as $setting => $value) {
            // Inject the param as env variables
            putenv("$setting=$value");
        }
    }
}