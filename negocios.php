<?php

class Negocios 
{
    public static function index($pagina, $registros)
    {
        // echo 'Imprimindo tipo pagina no negocios.php: '.gettype($pagina)."\n";
        // echo gettype($registros)."\n";
        $limit = $registros;
        $start = ($pagina - 1) * $limit;

        // $end = 112;
        // for ($i = 1; $i <= 7; $i++) {
        $cURLConnection = curl_init('https://api.moskitcrm.com/v2/deals/search?start=' . $start . '&limit=' . $limit . '&order=desc');
        curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($cURLConnection, CURLOPT_HTTPHEADER, array(
            'apikey: a4ca266a-ef70-462f-a5bd-abc6340928b0',
        ));

        $apiResponse = curl_exec($cURLConnection);
        curl_close($cURLConnection);

        $jsonObj = json_decode($apiResponse);

        // $end = $jsonObj->metadata->pagination->total;
        // $start = $start + 100;
        $result = $jsonObj;


       return $result; 
    }

}
?>