---
title: "Excelのアドインを作成しました"
date: 2014-10-10T10:55:53
slug: "excel_addin"
categories: ["コンピューター"]
tags: ["Excel","Microsoft","コンピューター"]
summary: "システムのバージョンアップに伴ない、アプリケーションのテストを実施する事になりました。 この作業は動作確認をしつつ、ひたすら画面のキャプチャーを取得してExcelに貼りつけるという単純な作業になります。とはいえ、完全に自動化して実施できるほど簡単でもなく、何度もやる必要のない仕事です。"
---

システムのバージョンアップに伴ない、アプリケーションのテストを実施する事になりました。

この作業は動作確認をしつつ、ひたすら画面のキャプチャーを取得してExcelに貼りつけるという単純な作業になります。とはいえ、完全に自動化して実施できるほど簡単でもなく、何度もやる必要のない仕事です。

そこで、すこしでも楽をしようとExcelのアドインを使って、キャプチャーした複数の画像ファイルをエクセルに一括で貼りつけるアドインを使用しました。  
アドインを使うと、提出用のExcelブックをマクロで汚すことなく、マクロと同じように作業を自動化できます。

もっともアドインを作って登録するまでが、かなり煩雑な手順が必要なのですが…。

ポイントとしては最近のExcelだと画像を挿入すると、画像そのものが貼られるのではなく、画像のリンクが貼られてしまうので、そのままでは提出用としては使いずらいものとなります。そこで一度貼りつけた画像をクリップボードにコピーして、再度同じ場所にペーストする事で、画像がリンクになる事を回避しています。(Excel上では後からではリンクを内部画像に変換できないようです)

元ネタはどこかの掲示板で取得したマクロです。先人の努力に感謝です。  
以下にそのソースを掲載します。

``` brush:
Sub 複数の画像を挿入()
'
' 複数の画像を挿入 Macro
'
' Keyboard Shortcut:
'
    Dim strFilter As String
    Dim Filenames As Variant
    Dim PIC       As Picture
    
     ' 「ファイルを開く」ダイアログでファイル名を取得
     strFilter = "画像ファイル(*.jpg;*.jpeg;*.gif;*.bmp;*.png),*.jpg;*.jpeg;*.gif;*.bmp;*.png"
    Filenames = Application.GetOpenFilename( _
                    FileFilter:=strFilter, _
                    Title:="図の挿入(複数選択可）", _
                    MultiSelect:=True)
    If Not IsArray(Filenames) Then Exit Sub
  
     ' ファイル名をソート
    Call BubbleSort_Str(Filenames, True, vbTextCompare)
    
     ' 貼り付け開始セルを選択
     'Range("C5").Select
    
     ' マクロ実行中の画面描写を停止
     Application.ScreenUpdating = False
    ' 順番に画像を挿入
     For i = LBound(Filenames) To UBound(Filenames)
        Set PIC = ActiveSheet.Pictures.Insert(Filenames(i))
      
         '-------------------------------------------------------------
        ' 画像の各種プロパティ変更
         '-------------------------------------------------------------
        With PIC
            .Top = ActiveCell.Top        ' 位置：アクティブセルの上側に重ねる
            .Left = ActiveCell.Left      ' 位置：アクティブセルの左側に重ねる
            .Placement = xlMove          ' 移動するがサイズ変更しない
            .PrintObject = True          ' 印刷する
        End With
        With PIC.ShapeRange
            .LockAspectRatio = msoTrue   ' 縦横比維持
            ' 画像の高さをアクティブセルにあわせる
            ' 結合セルの場合でも対応
            ' .Height = ActiveCell.MergeArea.Height
            .ScaleHeight 0.5, msoTrue
            .ZOrder msoSendToBack
        End With
        ActiveCell.Select
        'Set ActiveCell.Width = PIC.ShapeRange.Width
        Dim row, col As Integer
        row = ActiveCell.row
        col = ActiveCell.Column
        ActiveCell.ColumnWidth = PIC.ShapeRange.Width / 6
        PIC.CopyPicture
        PIC.Delete
        ActiveSheet.Paste
        
        Dim count As Integer
        count = ActiveSheet.Shapes.count
        ActiveSheet.Shapes(count - 1).ZOrder msoSendToBack

        ' 次の貼り付け先を選択（アクティブセルにする）[例：5個下のセル]
        'ActiveCell.Offset(5).Select
        ActiveCell.Offset(0, 2).Select
    
         Set PIC = Nothing
    Next i
  
     ' 終了
     Application.ScreenUpdating = True
    MsgBox i - 1 & "枚の画像を挿入しました", vbInformation

 End Sub

 ' バブルソート（文字列）
Private Sub BubbleSort_Str( _
    ByRef Source As Variant, _
    Optional ByVal SortAsc As Boolean = True, _
    Optional ByVal Compare As VbCompareMethod = vbTextCompare)
  
     If Not IsArray(Source) Then Exit Sub
  
     Dim i As Long, j As Long
    Dim vntTmp As Variant
    For i = LBound(Source) To UBound(Source) - 1
        For j = LBound(Source) To LBound(Source) + UBound(Source) - i - 1
            If StrComp(Source(IIf(SortAsc, j, j + 1)), _
                       Source(IIf(SortAsc, j + 1, j)), Compare) = 1 Then
                vntTmp = Source(j)
                Source(j) = Source(j + 1)
                Source(j + 1) = vntTmp
            End If
        Next j
    Next i

 End Sub

' ある一つのサブフォルダについての処理
Private Function importImagesFromOneSubDir(sub_dir, y, root_dir)
    'MsgBox sub_dir.Name
    
    ' このフォルダ内の画像をすべて列挙
    file_name = Dir(sub_dir & "\*.*")
    Do While file_name <> ""
        ' このファイルの拡張子を調べる
        If isImageFile(file_name) Then
            ' 画像であれば，取り込んで次の行へ
            importImageFile file_name, y, root_dir, sub_dir
            y = y + 1
        End If
        
        ' 次のファイルを取得
        file_name = Dir()
    Loop
        
    ' 現在の行を返す
    importImagesFromOneSubDir = y
    
End Function
        

' 画像ファイルかどうか，拡張子で判定する
Private Function isImageFile(file_name)
    
    ' ピリオドは後ろから何文字目か
    pos_period = InStrRev(file_name, ".")
    If pos_period > 0 Then
        ' 拡張子を切り出し
        file_ext = LCase(Mid(file_name, pos_period + 1))
        
        ' 画像の拡張子か？（小文字で指定可）
        If _
            file_ext = "jpg" Or _
            file_ext = "jpeg" Or _
            file_ext = "bmp" Or _
            file_ext = "gif" Or _
            file_ext = "png" _
        Then
            ' 画像であると判定
            ret = True
        Else
            ret = False
        End If
    Else
        ret = False
    End If
    ' http://officetanaka.net/excel/vba/tips/tips57.htm
    
    isImageFile = ret
End Function

' ある一つの画像ファイルをシート中に取り込む
Private Sub importImageFile(file_name, y, root_dir, sub_dir)
    file_path = sub_dir & "\" & file_name
    
    ' 一列目にはサブフォルダ名を
    ActiveSheet.Cells(y, 1).Value = sub_dir.Name
    
    ' 二列目には画像を
    ActiveSheet.Cells(y, 2).Select
    Set myShape = ActiveSheet.Shapes.AddPicture( _
          fileName:=file_path, _
          LinkToFile:=False, _
          SaveWithDocument:=True, _
          Left:=Selection.Left, _
          Top:=Selection.Top, _
          Width:=Application.CentimetersToPoints(6), _
          Height:=Application.CentimetersToPoints(1))
        ' http://www.moug.net/tech/exvba/0120020.html
        ' http://www.moug.net/tech/exvba/0070012.html
    
    ' この行高を自動調整
    Cells(y, 1).RowHeight = Application.CentimetersToPoints(1)

End Sub

 Sub picIns(ByVal r As Range, _
           ByVal s As String, _
           ByVal W As Single, _
           ByVal H As Single)

    With ActiveSheet.Pictures.Insert(s).ShapeRange
        If (W > 0) And (H > 0) Then
            .LockAspectRatio = msoFalse
            .Width = W
            .Height = H
        ElseIf W > 0 Then
            .Width = W
        ElseIf H > 0 Then
            .Height = H
        End If
        .Left = r.Left
        .Top = r.Top
    End With
 End Sub
```
