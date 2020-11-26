<?php
    include_once 'negocios.php';

    //verifica a página atual caso seja informada na URL, senão atribui como 1ª página 
    $pagina = (isset($_GET['pagina']))? $_GET['pagina'] : 1; 
    $pagina = intval($pagina);
    
    $registros = 10;
    $result = Negocios::index($pagina, $registros);

    if (count($result) != 10) {
        $total = $pagina;
    } else{
        $total = $pagina + 1;
    }

    //calcula o número de páginas arredondando o resultado para cima 
    $numPaginas = ceil($total/$registros); 
    $lim = 5;
    
    //variavel para calcular o início da visualização com base na página atual 
    $inicio = ((($pagina - $lim) > 1)? $pagina - $lim : 1); 
    $fim = ((($pagina+$lim) < $numPaginas) ? $pagina+$lim : $numPaginas);

?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Invexo</title>

    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="path/to/font-awesome/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

</head>
<body>  
    <div class="top">
        <div class="row align-items-center">
            <div class="col" >
                <img src="index.png" alt="..." class="img">
            </div>
        </div>

    </div>
    
    <div class="container-fluid">
    Pesquisar
        <div class="row">
        
            <div class="input-group col-md-4">
                <input type="text" class="form-control" placeholder="Digite ao menos 3 caracteres...">
                <div class="input-group-append">
                <button class="btn btn-secondary" type="button">
                    <i class="fa fa-search"></i>
                    
                </button>
                </div>
            </div>
        </div>
    
            <table class="table">
            <thead class="thead-dark">
                    <tr>
                        <th scope="col">Negócio</th>
                        <th scope="col">Empreendimento</th>
                        <th scope="col">Bairro</th>
                        <th scope="col">Origem</th>
                        <th scope="col">Qualificação</th>
                        <th scope="col">Horário Adicionado</th>
                        <th scope="col">Mensagem</th>
                    </tr>
                </thead>

                <tbody>
                    <?php foreach ($result as $user):
                        $date = explode('T', $user->dateCreated);
                        $dia = $date[0];
                        $hora = $date[1];

                        $d = explode('-', $dia)[2];
                        $m = explode('-', $dia)[1];
                        $a = explode('-', $dia)[0];
                        $finaldia = $d . '-'. $m . '-'. $a;

                        $horario = explode('.', $hora)[0];
                        $H = intval(explode(':', $horario)[0]) - 3;
                        $M = explode(':', $horario)[1];
                        $S = explode(':', $horario)[2];
                        $finalHora = $H . ':'. $M . ':' . $S;

                        $finalDate = $finaldia .' '. $finalHora ."\n";
                        $Negocio = '';
                        $Empreendimento = '';

                        if (strpos($user->name, '|')){
                            $name = explode('|', $user->name);
                            $Empreendimento = $name[1];
                            $Negocio = $name[0];
                        }
                    ?>
                    <tr>
                        <?php include_once 'customFields.php';
                        
                        $Bairro = '';
                        $Origem = '';
                        $Qualificação = '';
                        $Mensagem = '';
                        
                        foreach ($user->entityCustomFields as $values): 
                            if ($values->id == 'CF_42AmaJiZCW64LDjl'){
                                $Mensagem = $values->textValue;
                            }
                            if ($values->id == 'CF_ylAm0viKi37pqvbx'){
                                if ($Empreendimento == ''){
                                    $endpoint = '/customFields/CF_ylAm0viKi37pqvbx/options/' . $values->options[0];
                                    $value = CustomFields::index($endpoint);
                                    $Empreendimento = $value->label;
                                    $Negocio = $user->name;
                                }
                            }
                            if ($values->id  == 'CF_Pj3qYeidiNxLqQeb'){
                                $endpoint = '/customFields/CF_Pj3qYeidiNxLqQeb/options/'. $values->options[0]; 
                                $value = CustomFields::index($endpoint);
                                $Bairro = $value->label;
                            }
                            if ($values->id == 'CF_GwyMgWi9CWAzzMLA'){
                                $Origem = $values->textValue;
                            }
                            if ($values->id == 'CF_lXODObivipvANmaN'){
                                if ($values->options[0] == 165206){
                                    $Qualificação = 'Bom';
                                } else {
                                    $Qualificação = 'Ruim';
                                }
                            }
                        ?>
                        <?php endforeach ?>
                        <td scope="row"><?= $Negocio ?></td>
                        <td scope="row"><?= $Empreendimento  ?></td>
                        <td scope="row"><?= $Bairro  ?></td>
                        <td scope="row"><?= $Origem  ?></td>
                        <td scope="row"><?= $Qualificação  ?></td>
                        <td scope="row"><?= $finalDate ?></td>
                        <td scope="row"><?= $Mensagem  ?></td>
        
                    </tr>

                    <?php endforeach ?>
                </tbody>
            </table>

            <nav aria-label="Page navigation example">
            <ul class="pagination justify-content-center">
                <?php 
                    if ($numPaginas > 1 && $pagina <= $numPaginas){
                        for($i = $inicio; $i < $fim + 1; $i++) {
                ?>
                <a class="page-link" href="invexo.php?pagina=<?php echo $i; ?>"><?php echo $i ?></a>
                <?php
                    }
                }?>
            </ul>
            </nav>

    </div>

</body>
</html>