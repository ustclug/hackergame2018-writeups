<?php
$flag = "flag{G00G1E-is-always-YOUR-FRIEND}";

$questions = [
  ["中国科学技术大学的建校年份是？","1958"],
  ["你研究过中国科大学号的演变史吗？现有一位 1992 年入学的博士生，系别为 11 系，学生编号为 26，请问 Ta 的学号是？","9211B026"],
  ["视频《诺贝尔奖获得者和杰出科学家祝福科大60华诞》中，出现了多少位诺贝尔奖得主和世界顶尖科学家为中国科大六十周年华诞送上祝福？（数字）","9"],
  ["在中国科大图书馆中，有一本书叫做《程序员的自我修养:链接、装载与库》，请问它的索书号是？","TP311.1/94"],
  ["我校 Linux 用户协会在大约三年前曾经举办过一次小聚，其主题是《白帽子大赛，黑客不神秘》，请问这次小聚使用的教室编号是？","3A202"]
];
?>

<html>
<head>
<title>USTC Quiz</title>
</head>
<body>
<h1>中国科学技术大学知识竞赛</h1>
<?php
  if (isset($_POST['a'])){
    $cnt = 0;
    foreach ($questions as $i => $q) {
      if ($_POST['a'][$i] === $q[1]){
        $cnt++;
      }
    }
    echo "<p>答对了 $cnt 道题</p>";
    if ($cnt === count($questions)){
      echo $flag;
    }
  }
?>
<form method='POST'>
<ol>
  <?php foreach ($questions as $i => $q) {
    echo "<li>$q[0]</li>";
    echo "<input type='text' name='a[$i]'/>";
  } ?>

  <p><input type="submit" value="提交" /></p>
</ol>
</form>
</body>
</html>
