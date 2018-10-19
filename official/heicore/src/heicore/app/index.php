<?php
function isHeicoreLatest() {
  if(isset($_SERVER['HTTP_USER_AGENT'])) {
    $userAgent = $_SERVER['HTTP_USER_AGENT'];
    $keyword = "HEICORE/49.1.2623.213";
    if (strpos($userAgent, $keyword) !== false) {
      return true;
    }
  }
  return false;
}

$flag = "flag{H3ic0re_49.1.2623.213_sai_kou}";
?>

<html>
<head>
<title>FLAG.txt</title>
</head>
<body>
<h1>FLAG.txt</h1>
<? if (isHeicoreLatest()): ?>
<p>The flag is: <code><?=$flag?></code></p>
<? else: ?>
为了文档安全，请使用最新版本黑曜石浏览器（HEICORE）访问。
<? endif ?>
</body>
</html>