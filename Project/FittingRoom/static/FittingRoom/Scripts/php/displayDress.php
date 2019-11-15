<?php
    $dir = new RecursiveDirectoryIterator("/static/FittingRoom/Dresses/");

    foreach (new RecursiveIteratorIterator($dir) as $filename => $file)
    {
        echo $filename
    }
?>
