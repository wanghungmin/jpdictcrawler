# Anki Add-on:Japenese Dictionary Crawler 日中字典爬蟲


## Introduction 簡介

一個能自動生成解釋，發音，及例句的anki add-on。使用beautiful soup套件爬取滬江小d的網路日文辭典搜尋結果，包括：假名、解釋、發音、句子、句子解釋、句子發音，並自動填入對應欄位

An anki add-on which can generate meanings, pronounces and sentences automatically.Using the beautiful soup package to get the results of 滬江小d web japanese dictionary including kana,meaning,pronounce,sentence,sentence meaning,sentence pronounce,and it can generate the fields automatically

## Usage 使用方式
### config.json
自訂義來源欄位及目標欄位名稱，使用json格式
* noteTypes : 定義note名稱中需含有的字串
* srcFields : 定義來源欄位可能的名稱
* dstFields : 定義目標欄位的屬性及相對的名稱
    * MeaningFields : 定義解釋欄位的名稱
    * KanaFields: 定義假名欄位的名稱
    * PronounceAudioField : 定義發音欄位的名稱
    * SentenceFields : 定義句子欄位的名稱
    * SentenceMeaningFields : 定義句子解釋欄位的名稱
    * SentenceAudioField : 定義句子發音欄位的名稱

### 當有多個讀音時:
當有多個讀音時，會跳出選擇視窗供你選擇需要的讀音

## To do 仍待完成功能
* 加入add-on生成NoteType
* 切換生成的欄位的開關
* 切換繁簡轉換的開關
* 生成note時如有發音則播放一次

## Existing Problems 現有問題
* 當羅馬拼音不存在但有發音時(例如搜尋句子)，生成的audio欄位不正確(romanki is empty)
* 詞性變化的redirection

Copyright © 2019 wanghungmin 