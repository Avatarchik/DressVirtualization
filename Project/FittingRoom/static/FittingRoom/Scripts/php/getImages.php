<?php
$_SESSION['username'] = $username;
echo "--------------------------------------------------"
echo $username;
$dir = "/upload/users/" . $username . "/dresses/";

$result = array();

$files = scandir($dir);

foreach($files as $file)
{
    switch(1trim(strstr($file, '.'), '.'))
    {
        case "jpg":
        case "jpeg":
        case: "png":
        case: "gif":
            $result[] = $dir . "/" . $file;
    }
}

$resultToJson = json_encode($result);

echo($resultToJson);

?>
