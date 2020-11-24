<?php

class Negocios 
{
    public static function index($pagina, $registros)
    {
        $limit = $registros;
        $start = ($pagina - 1) * $limit;

        // $end = 112;
        // for ($i = 1; $i <= 7; $i++) {
        // $cURLConnection = curl_init('https://api.moskitcrm.com/v1/deals/?start=' . $start . '&limit=' . $limit . '&order=desc');
        // curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);
        // curl_setopt($cURLConnection, CURLOPT_HTTPHEADER, array(
        // 'apikey: a4ca266a-ef70-462f-a5bd-abc6340928b0',
        // ));

        // $apiResponse = curl_exec($cURLConnection);
        // curl_close($cURLConnection);

        // $jsonObj = json_decode($apiResponse);

        // // $end = $jsonObj->metadata->pagination->total;
        // // $start = $start + 100;
        // $result = $jsonObj;
        // API URL
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
        // echo gettype($payload);
        // echo $payload;
        // Attach encoded JSON string to the POST fields
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);

        // Set the content type to application/json
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json', 'apikey:168ec8df-5e4f-440f-b3cd-d03b1039dff7'));

        // Return response instead of outputting
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        // curl_setopt($ch, CURLINFO_HEADER_OUT, true);
        // curl_setopt($ch, CURLOPT_HEADER, true);

        // Execute the POST request
        $result = curl_exec($ch);
        
        // $teste = curl_getinfo($ch, CURLINFO_HEADER_OUT);
        // var_dump($teste);
        // $teste = curl_multi_getcontent($ch);

        // $header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        // $headers = substr($result, 0, $header_size);
        // $body = substr($result, $header_size);

        
        // print_r(apache_request_headers());

        // $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        // $header = substr($result, 0, $headerSize);
        // $header = getHeaders($header);

        // $headers = explode("\r\n", $headers); // The seperator used in the Response Header is CRLF (Aka. \r\n) 

        // $headers = array_filter($headers);

        // $html = '';
        // foreach ($headers as &$value) {
        //     $html .= '<li>' . $value . '</li>';
        // }
        // $html = '<ol>' . $html . '</ol>';

        // header("Content-Type:text/html; charset=UTF-8");
        // echo $html;
        // Close cURL resource
        curl_close($ch);

        $resultado = json_decode($result);


        // print_r($result);
        // echo gettype($result);
        // echo gettype($resultado);

        return $resultado; 
    }

}
?>