<?php
date_default_timezone_set("Asia/Shanghai");
session_start();
$flag = "flag{Evil_Integer._Evil_Overflow.}";

function clearAccount() {
  unset($_SESSION['account']);
}

function isExpired() {
  $create = $_SESSION['create'];
  $now = time();
  $ten_min = 60 * 10;
  if ($create + $ten_min <= $now)
    return true;
  return false;
}

function init() {
  if (!isset($_SESSION['account'])) {
    $_SESSION['account'] = substr(md5(mt_rand()), 0, 15);
    $_SESSION['create'] = time();
    $_SESSION['CTB'] = 10;
    $_SESSION['RMX'] = 0;
    $_SESSION['TDSU'] = 0;
    $_SESSION['FLAG'] = 0;
    $_SESSION['last_action'] = 0;
    $_SESSION['A1'] = 0;
    $_SESSION['A1_time'] = 0;
    $_SESSION['A1_profit'] = 0;
  }
}

function showtime($t = null) {
  if ($t == null)
    $t = time();
  echo "<!--DEBUG:". intval($t) ."-->";
  return date("Y-m-d H:i:s", intval($t));
}

function showinfo($msg) {
  return $msg;
}

function hasA1() {
  if ($_SESSION['A1_time'] === 0) {
    return false;
  }
  return true;
}

function check_balance($type, $num) {
  $balance = $_SESSION[$type];
  if ($balance < $num)
    die('余额不足，交易中止，点击<a href="/">这里</a>回到主页。');
}

function check_last_action() {
  $two_sec = 2;
  $now = time();
  if ($_SESSION['last_action'] + $two_sec >= $now) {
    die('交易过快，2 秒钟后再试，点击<a href="/">这里</a>回到主页。');
  }
  $_SESSION['last_action'] = time();
}

function action($t) {
  check_last_action();
  if ($t === "CTB2RMX") {
    check_balance('CTB', 1);
    $_SESSION['CTB'] -= 1;
    $_SESSION['RMX'] += 57;
  } else if ($t === "CTB2TDSU") {
    check_balance('CTB', 1);
    $_SESSION['CTB'] -= 1;
    $_SESSION['TDSU'] += 6606;
  } else if ($t === "RMX2CTB") {
    check_balance('RMX', 57);
    $_SESSION['RMX'] -= 57;
    $_SESSION['CTB'] += 1;
  } else if ($t === "RMX2TDSU") {
    check_balance('RMX', 1);
    $_SESSION['RMX'] -= 1;
    $_SESSION['TDSU'] += 115;
  } else if ($t === "TDSU2CTB") {
    check_balance('TDSU', 6606);
    $_SESSION['TDSU'] -= 6606;
    $_SESSION['CTB'] += 1;
  } else if ($t === "TDSU2RMX") {
    check_balance('TDSU', 115);
    $_SESSION['TDSU'] -= 115;
    $_SESSION['RMX'] += 1;
  } else if ($t === "buy_flag") {
    check_balance('CTB', 20);
    $_SESSION['CTB'] -= 20;
    $_SESSION['FLAG'] += 4;
  } else if ($t === "buy_flag_frag") {
    check_balance('CTB', 5);
    $_SESSION['CTB'] -= 5;
    $_SESSION['FLAG'] += 1;
  } else if ($t === "donate") {
    check_balance('TDSU', 1);
    $_SESSION['TDSU'] -= 1;
  } else if ($t === "buy_A1") {
    if (hasA1()) {
      die('已经购买，请勿重复购买，点击<a href="/">这里</a>回到主页。');
    }
    $val = intval($_GET['val']);
    $period_m = intval($_GET['period']);

    if (!($period_m >= 1)) {
      die('最少 1 分钟，点击<a href="/">这里</a>回到主页。');
    }

    if (!($val >= 1)) {
      die('份额至少 1 份，点击<a href="/">这里</a>回到主页。');
    }

    $period   = $period_m * 60;

    check_balance('TDSU', $val);
    $_SESSION['TDSU'] -= $val;
    $_SESSION['A1'] = $val;
    $_SESSION['A1_time'] = intval(time() + $period);
    $_SESSION['A1_profit'] = intval($period_m * 0.043 * $val);
  } else if ($t === "sell_A1") {
    if (!hasA1()) {
      die('未购买，点击<a href="/">这里</a>回到主页。');
    }

    $now = time();
    $t = $_SESSION['A1_time'];
    if ($now < $t) {
      die('未到取出时间，点击<a href="/">这里</a>回到主页。');
    }
    $_SESSION['TDSU'] += $_SESSION['A1'];
    $_SESSION['TDSU'] += $_SESSION['A1_profit'];
    $_SESSION['A1'] = 0;
    $_SESSION['A1_time'] = 0;
    $_SESSION['A1_profit'] = 0;
  }
}

function main() {
  init();
  if ($_GET['clear'] === 'y') {
    clearAccount();
    die('已经清空账号，请点击<a href="/">这里</a>重新开始。');
  }
  if (isExpired()) {
    clearAccount();
    die('账号已经过期，请点击<a href="/">这里</a>重新开始。');
  }
  if (isset($_GET['action'])) {
    action($_GET['action']);
  }
}

main();
?>
<html>
<head>
<style>
body {
  font-family: arial, sans-serif;
}
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}
</style>
</head>
<body>
<h1>Bank</h1>

<? if ($_SESSION['FLAG'] >= 4): ?>
<p>恭喜！</p>
<p>The flag is: <code><?=$flag?></code></p>
<? endif ?>

<p>每个账号仅有十分钟的有效期，初始为 10 CTB。</p>
<p>每个账号有三种货币：CTB，RMX，TDSU</p>
<h2>货币兑换</h2>
<table>
  <tr>
    <th>货币种类</th>
    <th>我的余额</th>
    <th>兑换 CTB</th>
    <th>兑换 RMX</th>
    <th>兑换 TDSU</th>
  </tr>
  <tr>
    <td>CTB</td>
    <td><?=$_SESSION['CTB']?></td>
    <td>1</td>
    <td><a href="?action=CTB2RMX">57</a></td>
    <td><a href="?action=CTB2TDSU">6606</a></td>
  </tr>
  <tr>
    <td>RMX</td>
    <td><?=$_SESSION['RMX']?></td>
    <td><a href="?action=RMX2CTB">1/57</a></td>
    <td>1</td>
    <td><a href="?action=RMX2TDSU">115</a></td>
  </tr>
  <tr>
    <td>TDSU</td>
    <td><?=$_SESSION['TDSU']?></td>
    <td><a href="?action=TDSU2CTB">1/6606</a></td>
    <td><a href="?action=TDSU2RMX">1/115</td>
    <td>1</td>
  </tr>
</table>
<h2>理财产品</h2>
<p>A1: 存入 TDSU，每分钟获得 4.3% 利息，最少一分钟。</p>
<? if(!hasA1()): ?>
<form method="get">
<input type="hidden" name="action" value="buy_A1">
<p>买入分钟：<input type="text" name="period" value="5"></p>
<p>买入份额：<input type="text" name="val" value="1000"></p>
<p><input type="submit" value="买入"></p>
</form>
<? else: ?>
<p>已买入</p>
<p>买入份额：<?=$_SESSION['A1']?> TDSU</p>
<p>预计收益：<?=$_SESSION['A1_profit']?> TDSU</p>
<p>取出时间：<?=showtime($_SESSION['A1_time'])?> 后</p>
<p><a href="?action=sell_A1">取出</a></p>
<? endif ?>
<h2>购买商品</h2>
<table>
  <tr>
    <th>商品类型</th>
    <th>价格</th>
    <th>购买</th>
  </tr>
  <tr>
    <td>FLAG</td>
    <td>20 CTB</td>
    <td><a href="?action=buy_flag">Buy</a></td>
  </tr>
  <tr>
    <td>FLAG 碎片(1/4)</td>
    <td>5 CTB</td>
    <td><a href="?action=buy_flag_frag">Buy</a></td>
  </tr>
  <tr>
    <td>爱心捐赠</td>
    <td>1 TDSU</td>
    <td><a href="?action=donate">Buy</a></td>
  </tr>
</table>

<p>账号：<?=$_SESSION['account']?>（<?=isExpired() ? "已过期" : "未过期" ?>）</p>
<p>创建时间：<?=showtime($_SESSION['create'])?></p>
<p>现在是：<?=showtime()?></p>
<p><a href="?clear=y">重新开始</a></p>
</body>
</html>