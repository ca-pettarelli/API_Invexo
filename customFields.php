<?php

class CustomFields 
{
    public static function index($endpoint)
    {
        $cURLConnection = curl_init('https://api.moskitcrm.com/v2' . $endpoint);
        curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($cURLConnection, CURLOPT_HTTPHEADER, array(
        'apikey: 168ec8df-5e4f-440f-b3cd-d03b1039dff7',
        ));

        $apiResponse = curl_exec($cURLConnection);
        curl_close($cURLConnection);

        $jsonObj = json_decode($apiResponse);

        $result = $jsonObj;

        return $result;

    }
}
?>