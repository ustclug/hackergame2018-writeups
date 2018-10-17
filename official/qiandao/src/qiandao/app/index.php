<?php
$flag = "flag{Hackergame2018_Have_Fun!}";
?>

<html>
<head>
<title>签到题</title>
</head>
<body>
<h1>签到题</h1>
<p> 本题的主要作用是向你展示获取 flag 的一般步骤：</p>
<ol>
  <li>打开题目页面；（也就是本页面，你应该已经完成了）</li>
  <li>解题；（找到 flag）</li>
  <li>回到比赛平台提交 flag；</li>
  <li>完成！</li>
</ol>
<p>是不是很简单！在本题中，你只要提交 <code>hackergame2018</code> 就可以得到 flag</p>
<form>
  <? if (isset($_GET['key'])): ?>
    <? if ($_GET['key'] == "hackergame2018"): ?>
      <p>The flag is: <code><?=$flag?></code></p>
    <? else: ?>
      <p>答案错误，正确的 Key 是：<code>hackergame2018</code></p>
    <? endif ?>
  <? endif ?>
  <p>Key: <input type="text" name="key" maxlength="13"/></p>
  <p><input type="submit" value="提交" /></p>
</form>
</body>
</html>