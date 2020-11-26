<?php

class Negocios 
{
    public static function index($pagina, $registros)
    {
        $limit = $registros;
        $start = ($pagina - 1) * $limit;

        $url = 'https://api.moskitcrm.com/v2/deals/search/?start' . $start . '&limit=' . $limit . '&order=desc';

        // Create a new cURL resource
        $ch = curl_init($url);

        // Setup request to send json via POST
        $data = array(
            'field' => 'CF_lXODObivipvANmaN',
            'expression' => 'all_of',
            'values' => array(165206),
        );
        // $payload = json_encode(array("user" => $data));
        $payload = json_encode($data);
        $payload = '['. $payload . ']';

        // Attach encoded JSON string to the POST fields
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);

        // Set the content type to application/json
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json', 'apikey:168ec8df-5e4f-440f-b3cd-d03b1039dff7'));

        // Return response instead of outputting
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        // Execute the POST request
        $result = curl_exec($ch);
        
        // Close cURL resource
        curl_close($ch);

        $resultado = json_decode($result);

        return $resultado; 
    }

}
?>