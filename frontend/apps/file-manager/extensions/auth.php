<?php
namespace IFM_Extensions;
use GuzzleHttp;

/**
 * Auth Controller
 * 
 * Extension to handle authentication between the interface and the file manager (i.e. for admin access)
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

class JWTAuth extends IFM_Extensions {
    function __construct() {
        // Set config
        $this->auth_cookie_name = 'access_token_cookie';
        $this->auth_env_var_name = 'LB_IFM_AUTHENTICATED';

        // Prepare guzzle client
        $this->client = new GuzzleHttp\Client();

        // Start authentication
        $this->authenticate();
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

        // If no token present, abort
        if (!$token) {
            $this->set_admin_mode(false);
            return false; 
        }

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
                $this->set_admin_mode(true);
                return true;
            } 

            // Otherwise, force disable auth
            $this->set_admin_mode(false);
        } catch (\Exception $e) {
            // An error occured, force disable auth
            // @TODO: Add proper error handling 
            $this->set_admin_mode(false);
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
        // Check that we have a cookie to work with 
        if (!isset($_COOKIE[$this->auth_cookie_name])) {
            // Otherwise, abort
            return false;
        }

        // Decode the JSON string saved in the cookie
        $token = filter_var($_COOKIE[$this->auth_cookie_name], FILTER_SANITIZE_STRING);

        // Check we have a token in here
        if (!isset($token)) {
            // Otherwise, abort
            return false;
        }
        
        // Finally, return the token for validation
        return $token;
    }



    /**
     * Set admin mode
     * 
     * Adds or removes a custom env variable for other extensions to use.
     * 
     * @param Boolean $success If auth was successful or not 
     * @return void.
     */

    private function set_admin_mode(bool $success) {
        if ($success) {
            // Auth succeeded
            putenv("{$this->auth_env_var_name}=true");
        } else {
            // Auth failed
            putenv("{$this->auth_env_var_name}=false");
        }
    }
}