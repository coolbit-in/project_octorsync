#OctoRsync
OctoRsync 是运行在[西电开源社区服务器](http://linux.xidian.edu.cn)上的软件源同步程序，相比于原有的 shell script + crontab 方式，OctoRsync 通过统一的调度管理，使软件源能够在恶劣的网络环境中**提高同步的成功率**。另外，原有的crontab设定了较长的同步间隔，使得一些更新量比较大的软件源，不得不一次同步非常长的时间，也增加了同步失败的概率。OctoRsync 可以自由设置同步间隔，默认为上次同步结束后120分钟再次请求同步，这样每天基本能同步5-6次。OctoRsync 还设置了并发限制，以防止平均带宽的减少导致同步失败。

##OctoRsync 配置文件说明
OctoRsync 的配置文件是 `config.ini`，使用`.ini`是因为 python 的`ConfigParser`模块可以直接解析，省的自己搞解析器了。
我尽可能的把配置文件搞得**简单易懂**，下面是添加一个软件源的语句块样例：
```
;发行版样例
;[发行版名称]
;EXCLUDE_FILE = 文件路径 (--exclude 参数文件)
;RSYNC_SERVER = rsync://XXXXXXXX/XXX
;MIRROR_ADDR = name
[ubuntu]
EXCLUDE_FILE = exclude_files/ubuntu.txt
RSYNC_SERVER = rsync://mirrors6.ustc.edu.cn/ubuntu
MIRROR_ADDR = ubuntu
```
如果要添加一个软件源，只需要添加这样一个语句块就可以了，然后你只需要启动它就可以了

##OctoRsync 产生的日志
OctoRsync 共生成了两种日志，一种是运行时日志，另一种是执行 Rsync 命令所产生的输出。

##OctoRsync 如何启动
```bash
$ sudo main.py &
```
见笑，以后会改进成系统服务的形式

##OctoRsync 的未来
还有很多东西需要改进，现在只是处于能用的阶段。大家若有兴趣欢迎一起来开发。

#LICENSE

Copyright (C) 2013 Coolbit Liu

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
