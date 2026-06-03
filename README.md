# BloodStrike-region-bypasser
[![GitHub stars](https://img.shields.io/github/stars/CN-Hobo/BloodStrike-region-bypasser?style=flat-square)](https://github.com/CN-Hobo/BloodStrike-region-bypasser/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/CN-Hobo/BloodStrike-region-bypasser?style=flat-square)](https://github.com/CN-Hobo/BloodStrike-region-bypasser/fork)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Language](https://img.shields.io/github/languages/top/CN-Hobo/BloodStrike-region-bypasser?style=flat-square)]()

> 第一个项目，不喜勿喷

## 📖 项目简介
针对于Steam端的游戏BloodStrike(译名:血战突袭)中登录时，非常非常简易的IP地区检测绕过工具。

## ✨ 主要原理
  1. 游戏启动时会向 https://mgbnaeast-g83naxx1ena.unisdk.easebar.com/g83naxx1ena/sdk/dlc_sync 发送POST请求
  2. 其中请求参数中包含参数名为"aim_info"，且参数值中包含"country":"国际代码"，当国际代码为CN时游戏将会提示不支持该地区
  3. 工具通过直接改掉"aim_info"这个标识，让游戏找不到地方来检查玩家的地区，从而实现可全程裸连

## 🚀 使用要求
### 环境依赖
- Windows & Python 3.8+
- 会python main.py
