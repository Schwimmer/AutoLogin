# AutoLogin
参考他人代码，通过配置文件自动ssh登录和scp传输文件

没有参数是ssh模式，有参数是scp模式
scp模式示例：
connect down /opt/pig_home/persona/DailyActivityPopulationPresentFeature.pig /home/david/code/audiences/persona/persona
然后再选择需要scp的服务器
如果是递归scp
connect down /opt/pig_home/persona /home/david/code/audiences/persona/persona 1
