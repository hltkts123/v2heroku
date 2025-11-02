' ============================================================================
' Module: DeleteSpecificSizedImages (Upgraded Version)
' Description: Xoa cac hinh anh co kich thuoc cu the trong PowerPoint
' Author: Upgraded Version
' Date: 2025-11-02
' Note: Tieng Viet khong dau de tranh loi encoding trong VBA Editor
' ============================================================================

Option Explicit

' Hang so
Private Const POINTS_PER_INCH As Single = 72
Private Const TOLERANCE As Single = 1 ' Dung sai (points)

' ============================================================================
' Main Procedure - Phien ban nang cap voi nhieu tinh nang moi
' ============================================================================
Sub DeleteSpecificSizedImages_Enhanced()
    On Error GoTo ErrorHandler
    
    Dim slide As slide
    Dim shape As shape
    Dim targetSizeInches As Single
    Dim targetSizePoints As Single
    Dim deletedCount As Long
    Dim totalImages As Long
    Dim shapeIndex As Long
    Dim userResponse As VbMsgBoxResult
    
    ' Khoi tao bien dem
    deletedCount = 0
    totalImages = 0
    
    ' Yeu cau nguoi dung nhap kich thuoc (tinh bang inch)
    Dim inputSize As String
    inputSize = InputBox("Nhap kich thuoc hinh anh can xoa (inch):", _
                         "Xoa hinh anh theo kich thuoc", "1.6")
    
    ' Kiem tra nguoi dung co huy khong
    If inputSize = "" Then
        MsgBox "Da huy thao tac.", vbInformation, "Thong bao"
        Exit Sub
    End If
    
    ' Chuyen doi va kiem tra gia tri nhap vao
    If Not IsNumeric(inputSize) Then
        MsgBox "Gia tri nhap vao khong hop le. Vui long nhap so.", vbExclamation, "Loi"
        Exit Sub
    End If
    
    targetSizeInches = CSng(inputSize)
    
    If targetSizeInches <= 0 Then
        MsgBox "Kich thuoc phai lon hon 0.", vbExclamation, "Loi"
        Exit Sub
    End If
    
    targetSizePoints = targetSizeInches * POINTS_PER_INCH
    
    ' Xac nhan truoc khi xoa
    userResponse = MsgBox("Ban co chac chan muon xoa tat ca hinh anh co kich thuoc " & _
                          targetSizeInches & " inch?" & vbCrLf & vbCrLf & _
                          "Thao tac nay khong the hoan tac!", _
                          vbYesNo + vbQuestion, "Xac nhan")
    
    If userResponse = vbNo Then
        MsgBox "Da huy thao tac.", vbInformation, "Thong bao"
        Exit Sub
    End If
    
    ' Duyet qua tung slide
    For Each slide In ActivePresentation.Slides
        ' Duyet nguoc de tranh loi khi xoa shape
        For shapeIndex = slide.Shapes.Count To 1 Step -1
            Set shape = slide.Shapes(shapeIndex)
            
            ' Kiem tra neu la hinh anh
            If shape.Type = msoPicture Or shape.Type = msoLinkedPicture Then
                totalImages = totalImages + 1
                
                ' Kiem tra kich thuoc voi dung sai
                If IsTargetSize(shape, targetSizePoints, TOLERANCE) Then
                    ' Ghi log thong tin shape truoc khi xoa (tuy chon)
                    Debug.Print "Da xoa: Slide " & slide.SlideIndex & _
                                ", Shape: " & shape.Name & _
                                ", Width: " & Round(shape.Width / POINTS_PER_INCH, 2) & "in" & _
                                ", Height: " & Round(shape.Height / POINTS_PER_INCH, 2) & "in"
                    
                    ' Xoa shape
                    shape.Delete
                    deletedCount = deletedCount + 1
                End If
            End If
        Next shapeIndex
    Next slide
    
    ' Hien thi ket qua
    MsgBox "Hoan tat!" & vbCrLf & vbCrLf & _
           "Tong so hinh anh: " & totalImages & vbCrLf & _
           "Da xoa: " & deletedCount & " hinh anh" & vbCrLf & _
           "Kich thuoc: " & targetSizeInches & " inch", _
           vbInformation, "Ket qua"
    
    Exit Sub

ErrorHandler:
    MsgBox "Da xay ra loi: " & Err.Description & vbCrLf & _
           "Ma loi: " & Err.Number, vbCritical, "Loi"
End Sub

' ============================================================================
' Function: Kiem tra xem shape co dung kich thuoc muc tieu khong
' ============================================================================
Private Function IsTargetSize(shape As shape, targetSize As Single, tolerance As Single) As Boolean
    IsTargetSize = (Abs(shape.Width - targetSize) < tolerance) Or _
                   (Abs(shape.Height - targetSize) < tolerance)
End Function

' ============================================================================
' Procedure: Phien ban don gian (giu nguyen logic goc, sua loi)
' ============================================================================
Sub DeleteSpecificSizedImages_Simple()
    On Error GoTo ErrorHandler
    
    Dim slide As slide
    Dim shape As shape
    Dim targetSize As Single
    Dim shapeIndex As Long
    
    ' Sua: Comment ghi 1.25 nhung code dung 1.6
    ' Da thong nhat su dung 1.6 inch
    targetSize = 1.6 * 72 ' 1.6 inch chuyen sang point (1 inch = 72 points)
    
    ' Duyet qua tung slide trong bai thuyet trinh
    For Each slide In ActivePresentation.Slides
        ' Duyet nguoc de tranh loi khi xoa shape
        ' (Quan trong: khi xoa shape, index cac shape sau se thay doi)
        For shapeIndex = slide.Shapes.Count To 1 Step -1
            Set shape = slide.Shapes(shapeIndex)
            
            ' Kiem tra neu la hinh anh va co kich thuoc mong muon
            If shape.Type = msoPicture Or shape.Type = msoLinkedPicture Then
                If (Abs(shape.Width - targetSize) < 1 Or Abs(shape.Height - targetSize) < 1) Then
                    shape.Delete
                End If
            End If
        Next shapeIndex
    Next slide
    
    MsgBox "Da xoa cac hinh anh co kich thuoc 1.6 inch!", vbInformation
    Exit Sub

ErrorHandler:
    MsgBox "Da xay ra loi: " & Err.Description, vbCritical, "Loi"
End Sub

' ============================================================================
' Procedure: Phien ban voi Progress Updates (tuy chon)
' ============================================================================
Sub DeleteSpecificSizedImages_WithProgress()
    On Error GoTo ErrorHandler
    
    Dim slide As slide
    Dim shape As shape
    Dim targetSize As Single
    Dim shapeIndex As Long
    Dim deletedCount As Long
    Dim totalSlides As Long
    Dim currentSlide As Long
    Dim progressInterval As Long
    
    targetSize = 1.6 * 72
    deletedCount = 0
    totalSlides = ActivePresentation.Slides.Count
    currentSlide = 0
    progressInterval = 10 ' Hien thi progress moi 10 slides
    
    ' Thong bao bat dau
    MsgBox "Bat dau xu ly " & totalSlides & " slides...", vbInformation, "Thong bao"
    
    For Each slide In ActivePresentation.Slides
        currentSlide = currentSlide + 1
        
        ' Hien thi tien trinh moi 10 slides (neu co nhieu slides)
        ' Chi ap dung neu > 20 slides de khong spam qua nhieu msgbox
        If totalSlides > 20 And currentSlide Mod progressInterval = 0 Then
            Debug.Print "Dang xu ly slide " & currentSlide & "/" & totalSlides & _
                        " - Da xoa: " & deletedCount & " hinh anh"
        End If
        
        For shapeIndex = slide.Shapes.Count To 1 Step -1
            Set shape = slide.Shapes(shapeIndex)
            
            If shape.Type = msoPicture Or shape.Type = msoLinkedPicture Then
                If (Abs(shape.Width - targetSize) < 1 Or Abs(shape.Height - targetSize) < 1) Then
                    shape.Delete
                    deletedCount = deletedCount + 1
                End If
            End If
        Next shapeIndex
    Next slide
    
    MsgBox "Hoan tat! Da xoa " & deletedCount & " hinh anh co kich thuoc 1.6 inch." & vbCrLf & _
           "Tong cong xu ly: " & totalSlides & " slides", _
           vbInformation, "Ket qua"
    Exit Sub

ErrorHandler:
    MsgBox "Da xay ra loi: " & Err.Description, vbCritical, "Loi"
End Sub

' ============================================================================
' Procedure: Phien ban voi tuy chon nang cao
' ============================================================================
Sub DeleteSpecificSizedImages_Advanced()
    On Error GoTo ErrorHandler
    
    Dim slide As slide
    Dim shape As shape
    Dim targetWidth As Single
    Dim targetHeight As Single
    Dim targetWidthPoints As Single
    Dim targetHeightPoints As Single
    Dim matchMode As String
    Dim deletedCount As Long
    Dim shapeIndex As Long
    Dim inputWidth As String
    Dim inputHeight As String
    
    ' Buoc 1: Cho phep nguoi dung chon che do so khop
    matchMode = InputBox("Chon che do so khop:" & vbCrLf & vbCrLf & _
                         "1 - Xoa khi width HOAC height khop" & vbCrLf & _
                         "2 - Xoa khi CA width VA height khop" & vbCrLf & _
                         "3 - Xoa khi CHI width khop" & vbCrLf & _
                         "4 - Xoa khi CHI height khop", _
                         "Che do so khop", "1")
    
    If matchMode = "" Or Not IsNumeric(matchMode) Then Exit Sub
    If Val(matchMode) < 1 Or Val(matchMode) > 4 Then
        MsgBox "Lua chon khong hop le! Vui long chon tu 1-4.", vbExclamation, "Loi"
        Exit Sub
    End If
    
    ' Buoc 2: Nhap kich thuoc width (neu can)
    If matchMode = "1" Or matchMode = "2" Or matchMode = "3" Then
        inputWidth = InputBox("Nhap chieu RONG (width) can xoa (inch):" & vbCrLf & _
                              "Vi du: 1.6", _
                              "Nhap chieu rong", "1.6")
        
        If inputWidth = "" Then Exit Sub
        
        If Not IsNumeric(inputWidth) Then
            MsgBox "Gia tri width khong hop le! Vui long nhap so.", vbExclamation, "Loi"
            Exit Sub
        End If
        
        targetWidth = CSng(inputWidth)
        If targetWidth <= 0 Then
            MsgBox "Kich thuoc width phai lon hon 0!", vbExclamation, "Loi"
            Exit Sub
        End If
        targetWidthPoints = targetWidth * POINTS_PER_INCH
    End If
    
    ' Buoc 3: Nhap kich thuoc height (neu can)
    If matchMode = "1" Or matchMode = "2" Or matchMode = "4" Then
        inputHeight = InputBox("Nhap chieu CAO (height) can xoa (inch):" & vbCrLf & _
                               "Vi du: 1.6", _
                               "Nhap chieu cao", "1.6")
        
        If inputHeight = "" Then Exit Sub
        
        If Not IsNumeric(inputHeight) Then
            MsgBox "Gia tri height khong hop le! Vui long nhap so.", vbExclamation, "Loi"
            Exit Sub
        End If
        
        targetHeight = CSng(inputHeight)
        If targetHeight <= 0 Then
            MsgBox "Kich thuoc height phai lon hon 0!", vbExclamation, "Loi"
            Exit Sub
        End If
        targetHeightPoints = targetHeight * POINTS_PER_INCH
    End If
    
    ' Buoc 4: Xac nhan truoc khi xoa
    Dim confirmMsg As String
    Select Case matchMode
        Case "1"
            confirmMsg = "Xoa hinh co width = " & targetWidth & " inch HOAC height = " & targetHeight & " inch"
        Case "2"
            confirmMsg = "Xoa hinh co width = " & targetWidth & " inch VA height = " & targetHeight & " inch"
        Case "3"
            confirmMsg = "Xoa hinh co width = " & targetWidth & " inch"
        Case "4"
            confirmMsg = "Xoa hinh co height = " & targetHeight & " inch"
    End Select
    
    If MsgBox("Ban co chac chan muon:" & vbCrLf & vbCrLf & _
              confirmMsg & "?" & vbCrLf & vbCrLf & _
              "Thao tac nay khong the hoan tac!", _
              vbYesNo + vbQuestion, "Xac nhan") = vbNo Then
        MsgBox "Da huy thao tac.", vbInformation, "Thong bao"
        Exit Sub
    End If
    
    ' Buoc 5: Xu ly xoa hinh anh
    deletedCount = 0
    
    For Each slide In ActivePresentation.Slides
        For shapeIndex = slide.Shapes.Count To 1 Step -1
            Set shape = slide.Shapes(shapeIndex)
            
            If shape.Type = msoPicture Or shape.Type = msoLinkedPicture Then
                Dim shouldDelete As Boolean
                shouldDelete = False
                
                Select Case matchMode
                    Case "1" ' Width HOAC Height
                        shouldDelete = (Abs(shape.Width - targetWidthPoints) < TOLERANCE) Or _
                                      (Abs(shape.Height - targetHeightPoints) < TOLERANCE)
                    Case "2" ' Width VA Height
                        shouldDelete = (Abs(shape.Width - targetWidthPoints) < TOLERANCE) And _
                                      (Abs(shape.Height - targetHeightPoints) < TOLERANCE)
                    Case "3" ' Chi Width
                        shouldDelete = (Abs(shape.Width - targetWidthPoints) < TOLERANCE)
                    Case "4" ' Chi Height
                        shouldDelete = (Abs(shape.Height - targetHeightPoints) < TOLERANCE)
                End Select
                
                If shouldDelete Then
                    ' Ghi log
                    Debug.Print "Da xoa: Slide " & slide.SlideIndex & _
                                ", Shape: " & shape.Name & _
                                ", Width: " & Round(shape.Width / POINTS_PER_INCH, 2) & "in" & _
                                ", Height: " & Round(shape.Height / POINTS_PER_INCH, 2) & "in"
                    
                    shape.Delete
                    deletedCount = deletedCount + 1
                End If
            End If
        Next shapeIndex
    Next slide
    
    ' Buoc 6: Hien thi ket qua
    MsgBox "Hoan tat!" & vbCrLf & vbCrLf & _
           "Da xoa: " & deletedCount & " hinh anh" & vbCrLf & _
           confirmMsg, _
           vbInformation, "Ket qua"
    Exit Sub

ErrorHandler:
    MsgBox "Da xay ra loi: " & Err.Description, vbCritical, "Loi"
End Sub
