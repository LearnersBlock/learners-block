<?php
namespace IFM_Extensions;
use GuzzleHttp;
use Guzzle\Http\Exception\ClientErrorResponseException;

/**
 * JWT Auth Controller
 * 
 * Controller to handle JWT authentication between app and filemanager
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

class JWTAuth extends IFM_Extensions {
    function __construct() {
        // config
        $this->auth_cookie_name = 'lb__auth';

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

        // prepare guzzle client
        $this->client = new GuzzleHttp\Client();

        // start authentication
        $this->is_auth_enabled();
    }



    /**
     * is_auth_enabled
     * 
     * Checks whether or not the filemanager admin mode has been enabled
     * via the"mode=admin" URL parameter. If so, run the auth process.
    */

    private function is_auth_enabled () {
        if (isset($_GET['mode'])) {
            // store url param
            $mode = (string) $_GET['mode'];

            // now check
            if ($mode === 'admin') {
                $this->authenticate();
            }
        }
    }



    /**
     * authenticate
     * 
     * Runs the authentication process by validating the store token using the
     * backend API. If authentication fails, authentication via the login form is forced.
    */

    private function authenticate() {
        // get the token
        $token = $this->get_token_from_cookie();

        // check if we have a token
        if ($token) {
            try {
                // if so, time to verify it
                // run POST request to JWT auth endpoint
                $response = $this->client->request(
                    'POST',
                    $_ENV['BACKEND_API_BASE'] . '/v1/auth/validate',
                    [
                        'form_params' => [
                            'token' => $token
                        ]
                    ]
                );

                // token verification was a success
                $body = $response->getBody();

                // make sure we have the correct response
                if ($response->getStatusCode() == 200) {
                    //  and enable the admin mode
                    $this->enable_admin_mode();
                }
            } catch(\GuzzleHttp\Exception\GuzzleException $e) {
                // handle exception
                // check that we have a response
                if ($e->hasResponse()) {
                    // if so, get the error response body
                    $body = $e->getResponse()->getBody();
                    $response = $body->getContents();
                    $response = json_decode($response);

                    // check if this is a auth error
                    if (isset($response->status) && $response->status === 401) {
                        // if so, force logout and ask for re-login
                        header('Location: /#/logout?redirect=/login?redirect=/files/admin'); 
                    }
                }
            }
        } else {
            // otherwise, if no cookie present, force login
            header('Location: /#/login?redirect=/files/admin'); 
        }
    }



    /**
     * get_token_from_cookie
     * 
     * Fetches the token from the auth cookie and returns it to the
     * authentication function to validate it.
    */

    private function get_token_from_cookie () {
        if (isset($_COOKIE[$this->auth_cookie_name])) {
            // decode the JSON string saved in the cookie
            $cookie_content = json_decode($_COOKIE[$this->auth_cookie_name]);

            // check we have a token in here
            if (isset($cookie_content->token)) {
                // if so, return it
                return $cookie_content->token;
            }
            
            // otherwise, return false
            return false;
        }
    }



    /**
     * enable_admin_mode
     * 
     * Adds all the env varaibles required to enable the filemanager admin mode
     * based on the parameters defined in the constructor.
    */

    private function enable_admin_mode() {
        // loop over all admin params
        foreach($this->admin_params as $setting => $value) {
            // inject the params as env variables
            putenv("$setting=$value");
        }
    }
}