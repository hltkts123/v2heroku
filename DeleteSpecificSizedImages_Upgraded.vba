' ============================================================================
' Module: DeleteSpecificSizedImages (Upgraded Version)
' Description: X?a c?c h?nh ?nh c? k?ch th??c c? th? trong PowerPoint
' Author: Upgraded Version
' Date: 2025-11-02
' ============================================================================

Option Explicit

' H?ng s?
Private Const POINTS_PER_INCH As Single = 72
Private Const TOLERANCE As Single = 1 ' Dung sai (points)

' ============================================================================
' Main Procedure - Phi?n b?n n?ng c?p v?i nhi?u t?nh n?ng m?i
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
    
    ' Kh?i t?o bi?n ??m
    deletedCount = 0
    totalImages = 0
    
    ' Y?u c?u ng??i d?ng nh?p k?ch th??c (t?nh b?ng inch)
    Dim inputSize As String
    inputSize = InputBox("Nh?p k?ch th??c h?nh ?nh c?n x?a (inch):", _
                         "X?a h?nh ?nh theo k?ch th??c", "1.6")
    
    ' Ki?m tra ng??i d?ng c? h?y kh?ng
    If inputSize = "" Then
        MsgBox "?? h?y thao t?c.", vbInformation, "Th?ng b?o"
        Exit Sub
    End If
    
    ' Chuy?n ??i v? ki?m tra gi? tr? nh?p v?o
    If Not IsNumeric(inputSize) Then
        MsgBox "Gi? tr? nh?p v?o kh?ng h?p l?. Vui l?ng nh?p s?.", vbExclamation, "L?i"
        Exit Sub
    End If
    
    targetSizeInches = CSng(inputSize)
    
    If targetSizeInches <= 0 Then
        MsgBox "K?ch th??c ph?i l?n h?n 0.", vbExclamation, "L?i"
        Exit Sub
    End If
    
    targetSizePoints = targetSizeInches * POINTS_PER_INCH
    
    ' X?c nh?n tr??c khi x?a
    userResponse = MsgBox("B?n c? ch?c ch?n mu?n x?a t?t c? h?nh ?nh c? k?ch th??c " & _
                          targetSizeInches & " inch?" & vbCrLf & vbCrLf & _
                          "Thao t?c n?y kh?ng th? ho?n t?c!", _
                          vbYesNo + vbQuestion, "X?c nh?n")
    
    If userResponse = vbNo Then
        MsgBox "?? h?y thao t?c.", vbInformation, "Th?ng b?o"
        Exit Sub
    End If
    
    ' T?t c?p nh?t m?n h?nh ?? t?ng t?c ?? x? l?
    Application.ScreenUpdating = False
    
    ' Duy?t qua t?ng slide
    For Each slide In ActivePresentation.Slides
        ' Duy?t ng??c ?? tr?nh l?i khi x?a shape
        For shapeIndex = slide.Shapes.Count To 1 Step -1
            Set shape = slide.Shapes(shapeIndex)
            
            ' Ki?m tra n?u l? h?nh ?nh
            If shape.Type = msoPicture Or shape.Type = msoLinkedPicture Then
                totalImages = totalImages + 1
                
                ' Ki?m tra k?ch th??c v?i dung sai
                If IsTargetSize(shape, targetSizePoints, TOLERANCE) Then
                    ' Ghi log th?ng tin shape tr??c khi x?a (t?y ch?n)
                    Debug.Print "?? x?a: Slide " & slide.SlideIndex & _
                                ", Shape: " & shape.Name & _
                                ", Width: " & Round(shape.Width / POINTS_PER_INCH, 2) & "in" & _
                                ", Height: " & Round(shape.Height / POINTS_PER_INCH, 2) & "in"
                    
                    ' X?a shape
                    shape.Delete
                    deletedCount = deletedCount + 1
                End If
            End If
        Next shapeIndex
    Next slide
    
    ' B?t l?i c?p nh?t m?n h?nh
    Application.ScreenUpdating = True
    
    ' Hi?n th? k?t qu?
    MsgBox "Ho?n t?t!" & vbCrLf & vbCrLf & _
           "T?ng s? h?nh ?nh: " & totalImages & vbCrLf & _
           "?? x?a: " & deletedCount & " h?nh ?nh" & vbCrLf & _
           "K?ch th??c: " & targetSizeInches & " inch", _
           vbInformation, "K?t qu?"
    
    Exit Sub

ErrorHandler:
    Application.ScreenUpdating = True
    MsgBox "?? x?y ra l?i: " & Err.Description & vbCrLf & _
           "M? l?i: " & Err.Number, vbCritical, "L?i"
End Sub

' ============================================================================
' Function: Ki?m tra xem shape c? ??ng k?ch th??c m?c ti?u kh?ng
' ============================================================================
Private Function IsTargetSize(shape As shape, targetSize As Single, tolerance As Single) As Boolean
    IsTargetSize = (Abs(shape.Width - targetSize) < tolerance) Or _
                   (Abs(shape.Height - targetSize) < tolerance)
End Function

' ============================================================================
' Procedure: Phi?n b?n ??n gi?n (gi? nguy?n logic g?c, s?a l?i)
' ============================================================================
Sub DeleteSpecificSizedImages_Simple()
    On Error GoTo ErrorHandler
    
    Dim slide As slide
    Dim shape As shape
    Dim targetSize As Single
    Dim shapeIndex As Long
    
    ' S?a: Comment ghi 1.25 nh?ng code d?ng 1.6
    ' ?? th?ng nh?t s? d?ng 1.6 inch
    targetSize = 1.6 * 72 ' 1.6 inch chuy?n sang point (1 inch = 72 points)
    
    ' Duy?t qua t?ng slide trong b?i thuy?t tr?nh
    For Each slide In ActivePresentation.Slides
        ' Duy?t ng??c ?? tr?nh l?i khi x?a shape
        ' (Quan tr?ng: khi x?a shape, index c?c shape sau s? thay ??i)
        For shapeIndex = slide.Shapes.Count To 1 Step -1
            Set shape = slide.Shapes(shapeIndex)
            
            ' Ki?m tra n?u l? h?nh ?nh v? c? k?ch th??c mong mu?n
            If shape.Type = msoPicture Or shape.Type = msoLinkedPicture Then
                If (Abs(shape.Width - targetSize) < 1 Or Abs(shape.Height - targetSize) < 1) Then
                    shape.Delete
                End If
            End If
        Next shapeIndex
    Next slide
    
    MsgBox "?? x?a c?c h?nh ?nh c? k?ch th??c 1.6 inch!", vbInformation
    Exit Sub

ErrorHandler:
    MsgBox "?? x?y ra l?i: " & Err.Description, vbCritical, "L?i"
End Sub

' ============================================================================
' Procedure: Phi?n b?n v?i Progress Bar (t?y ch?n)
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
    
    targetSize = 1.6 * 72
    deletedCount = 0
    totalSlides = ActivePresentation.Slides.Count
    currentSlide = 0
    
    Application.ScreenUpdating = False
    
    For Each slide In ActivePresentation.Slides
        currentSlide = currentSlide + 1
        
        ' Hi?n th? ti?n tr?nh trong status bar
        Application.StatusBar = "?ang x? l? slide " & currentSlide & "/" & totalSlides & _
                                " - ?? x?a: " & deletedCount & " h?nh ?nh..."
        
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
    
    Application.ScreenUpdating = True
    Application.StatusBar = False ' Reset status bar
    
    MsgBox "Ho?n t?t! ?? x?a " & deletedCount & " h?nh ?nh c? k?ch th??c 1.6 inch.", _
           vbInformation, "K?t qu?"
    Exit Sub

ErrorHandler:
    Application.ScreenUpdating = True
    Application.StatusBar = False
    MsgBox "?? x?y ra l?i: " & Err.Description, vbCritical, "L?i"
End Sub

' ============================================================================
' Procedure: Phi?n b?n v?i t?y ch?n n?ng cao
' ============================================================================
Sub DeleteSpecificSizedImages_Advanced()
    On Error GoTo ErrorHandler
    
    Dim slide As slide
    Dim shape As shape
    Dim targetWidth As Single
    Dim targetHeight As Single
    Dim matchMode As String
    Dim deletedCount As Long
    Dim shapeIndex As Long
    
    ' Cho ph?p ng??i d?ng ch?n ch? ?? so kh?p
    matchMode = InputBox("Ch?n ch? ?? so kh?p:" & vbCrLf & _
                         "1 - X?a khi width HO?C height kh?p" & vbCrLf & _
                         "2 - X?a khi C? width V? height kh?p" & vbCrLf & _
                         "3 - X?a khi width kh?p" & vbCrLf & _
                         "4 - X?a khi height kh?p", _
                         "Ch? ?? so kh?p", "1")
    
    If matchMode = "" Or Not IsNumeric(matchMode) Then Exit Sub
    
    targetWidth = 1.6 * 72
    targetHeight = 1.6 * 72
    deletedCount = 0
    
    Application.ScreenUpdating = False
    
    For Each slide In ActivePresentation.Slides
        For shapeIndex = slide.Shapes.Count To 1 Step -1
            Set shape = slide.Shapes(shapeIndex)
            
            If shape.Type = msoPicture Or shape.Type = msoLinkedPicture Then
                Dim shouldDelete As Boolean
                shouldDelete = False
                
                Select Case matchMode
                    Case "1" ' Width HO?C Height
                        shouldDelete = (Abs(shape.Width - targetWidth) < 1) Or _
                                      (Abs(shape.Height - targetHeight) < 1)
                    Case "2" ' Width V? Height
                        shouldDelete = (Abs(shape.Width - targetWidth) < 1) And _
                                      (Abs(shape.Height - targetHeight) < 1)
                    Case "3" ' Ch? Width
                        shouldDelete = (Abs(shape.Width - targetWidth) < 1)
                    Case "4" ' Ch? Height
                        shouldDelete = (Abs(shape.Height - targetHeight) < 1)
                End Select
                
                If shouldDelete Then
                    shape.Delete
                    deletedCount = deletedCount + 1
                End If
            End If
        Next shapeIndex
    Next slide
    
    Application.ScreenUpdating = True
    
    MsgBox "?? x?a " & deletedCount & " h?nh ?nh!", vbInformation, "K?t qu?"
    Exit Sub

ErrorHandler:
    Application.ScreenUpdating = True
    MsgBox "?? x?y ra l?i: " & Err.Description, vbCritical, "L?i"
End Sub
