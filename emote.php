<?php

include('Eklekt/Emotion.php');
include('Eklekt/Emotion/AffectWord.php');
include('Eklekt/Emotion/EmotionalState.php');
include('Eklekt/Emotion/Empathyscope.php');
include('Eklekt/Emotion/Utility/Heuristics.php');
include('Eklekt/Emotion/Utility/Lexical.php');

#const NEUTRAL = -1;
#const HAPPINESS = 0;
#const SADNESS = 1;
#const FEAR = 2;
#const ANGER = 3;
#const DISGUST = 4;
#const SURPRISE = 5;

$wnaffect ='http://gsi.dit.upm.es/ontologies/wnaffect/ns'; 
$arr = array(
    -1 => $wnaffect.'#neutral-emotion',
    0 => $wnaffect.'#happiness',
    1 => $wnaffect.'#sadness',
    2 => $wnaffect.'#fear',
    3 => $wnaffect.'#anger',
    4 => $wnaffect.'#disgust',
    5 => $wnaffect.'#surprise'
);
$empathScope = Eklekt_Emotion_Empathyscope::getInstance();
$text = $_GET['q']?$_GET['q']:'Input a string with the ?q="bla" parameter, please';
$domain = $_GET['domain']?$_GET['domain']:'http://gsi.dit.upm.es/ontologies/wndomains/ns#Root';
$sens = explode(".", $text);
$res = array();
header('Content-Type: application/xml');
#header('Content-Disposition: attachment; filename="results.rdf"');
header('Content-Type: text/plain');
echo '<?xml version="1.0"?>';
?>
<rdf:RDF
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
  xmlns:prov="http://www.w3.org/ns/prov#"
  xmlns:wnaffect="http://gsi.dit.upm.es/ontologies/wnaffect/ns#"
  xmlns:wndomains="http://gsi.dit.upm.es/ontologies/wndomains/ns#"
  xmlns:onyx="http://gsi.dit.upm.es/ontologies/onyx#"
>
    <rdf:Description>
    <rdf:type rdf:resource="http://gsi.dit.upm.es/ontologies/onyx/ns#EmotionAnalysis<?echo $i?>"/> 
        <onyx:emotionOntology><? echo $wnaffect ?></onyx:emotionOntology> 
        <onyx:domain rdf:resource="<?echo $domain?>"/>
        <onyx:algorithm>Synesketch</onyx:algorithm>
    </rdf:Description>

    <rdf:Description xmlns:about="http://gsi.dit.upm.es">
        <rdf:type rdf:resource="http://www.w3.org/ns/prov#Agent"/> 
    </rdf:Description>

<?
for($i=0; $i<count($sens); $i++){
    $feel = $empathScope->feel($sen);
    foreach($feel->emotions as $emo){
        $emo->type = array_key_exists($emo->type, $arr)?$arr[$emo->type]:"UNKNOWN";
    }
    array_push($res, $feel);
?>
    <rdf:Description>
    <rdf:type rdf:resource="http://gsi.dit.upm.es/ontologies/onyx/ns#EmotionResult<?echo $i?>"/> 
        <onyx:sourceText><? echo $feel->text?></onyx:sourceText> 
        <onyx:domain rdf:resource="<?echo $domain?>"/>
        <onyx:hasEmotion>
            <onyx:Emotion>
                <onyx:emotionCategory rdf:resource="<? echo $emo->type?>"/> 
                <onyx:hasIntensity rdf:datatype="http://www.w3.org/2001/XMLSchema#float"><?echo $emo->weight?></onyx:hasIntensity> 
            </onyx:Emotion>
        </onyx:hasEmotion>
    </rdf:Description>
<?
}
?>
</rdf:RDF>

