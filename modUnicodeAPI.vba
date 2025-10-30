Option Explicit

' ===========================
' MODULE: modUnicodeAPI
' Mô tả: Windows API để xử lý Unicode cho tiếng Việt
' ===========================

' ============================================
' WINDOWS API DECLARATIONS
' ============================================

' API cho Unicode string conversion
#If VBA7 Then
    ' Office 2010 trở lên (64-bit compatible)
    
    Private Declare PtrSafe Function MultiByteToWideChar Lib "kernel32" ( _
        ByVal CodePage As Long, _
        ByVal dwFlags As Long, _
        ByVal lpMultiByteStr As String, _
        ByVal cchMultiByte As Long, _
        ByVal lpWideCharStr As String, _
        ByVal cchWideChar As Long) As Long
    
    Private Declare PtrSafe Function WideCharToMultiByte Lib "kernel32" ( _
        ByVal CodePage As Long, _
        ByVal dwFlags As Long, _
        ByVal lpWideCharStr As String, _
        ByVal cchWideChar As Long, _
        ByVal lpMultiByteStr As String, _
        ByVal cchMultiByte As Long, _
        ByVal lpDefaultChar As Long, _
        ByVal lpUsedDefaultChar As Long) As Long
    
    Private Declare PtrSafe Function SendMessageW Lib "user32" ( _
        ByVal hWnd As LongPtr, _
        ByVal wMsg As Long, _
        ByVal wParam As LongPtr, _
        ByVal lParam As LongPtr) As LongPtr
    
    Private Declare PtrSafe Function FindWindowA Lib "user32" ( _
        ByVal lpClassName As String, _
        ByVal lpWindowName As String) As LongPtr
    
    Private Declare PtrSafe Function GetWindowTextW Lib "user32" ( _
        ByVal hWnd As LongPtr, _
        ByVal lpString As String, _
        ByVal cch As Long) As Long
    
    Private Declare PtrSafe Function SetWindowTextW Lib "user32" ( _
        ByVal hWnd As LongPtr, _
        ByVal lpString As String) As Long
        
#Else
    ' Office 2007 và cũ hơn (32-bit)
    
    Private Declare Function MultiByteToWideChar Lib "kernel32" ( _
        ByVal CodePage As Long, _
        ByVal dwFlags As Long, _
        ByVal lpMultiByteStr As String, _
        ByVal cchMultiByte As Long, _
        ByVal lpWideCharStr As String, _
        ByVal cchWideChar As Long) As Long
    
    Private Declare Function WideCharToMultiByte Lib "kernel32" ( _
        ByVal CodePage As Long, _
        ByVal dwFlags As Long, _
        ByVal lpWideCharStr As String, _
        ByVal cchWideChar As Long, _
        ByVal lpMultiByteStr As String, _
        ByVal cchMultiByte As Long, _
        ByVal lpDefaultChar As Long, _
        ByVal lpUsedDefaultChar As Long) As Long
    
    Private Declare Function SendMessageW Lib "user32" ( _
        ByVal hWnd As Long, _
        ByVal wMsg As Long, _
        ByVal wParam As Long, _
        ByVal lParam As Long) As Long
    
    Private Declare Function FindWindowA Lib "user32" ( _
        ByVal lpClassName As String, _
        ByVal lpWindowName As String) As Long
    
    Private Declare Function GetWindowTextW Lib "user32" ( _
        ByVal hWnd As Long, _
        ByVal lpString As String, _
        ByVal cch As Long) As Long
    
    Private Declare Function SetWindowTextW Lib "user32" ( _
        ByVal hWnd As Long, _
        ByVal lpString As String) As Long
        
#End If

' ============================================
' CONSTANTS
' ============================================

Private Const CP_ACP = 0        ' ANSI code page
Private Const CP_UTF8 = 65001   ' UTF-8 code page
Private Const CP_UNICODE = 1200 ' Unicode

Private Const WM_SETTEXT = &HC
Private Const WM_GETTEXT = &HD

' ============================================
' PUBLIC FUNCTIONS
' ============================================

' Chuyển đổi string sang UTF-8
Public Function StringToUTF8(ByVal strInput As String) As String
    Dim lngLength As Long
    Dim strOutput As String
    
    On Error GoTo ErrHandler
    
    If Len(strInput) = 0 Then
        StringToUTF8 = ""
        Exit Function
    End If
    
    ' Tính độ dài cần thiết
    lngLength = WideCharToMultiByte(CP_UTF8, 0, strInput, -1, vbNullString, 0, 0, 0)
    
    If lngLength > 0 Then
        strOutput = String$(lngLength - 1, vbNullChar)
        WideCharToMultiByte CP_UTF8, 0, strInput, -1, strOutput, lngLength, 0, 0
        StringToUTF8 = strOutput
    Else
        StringToUTF8 = strInput
    End If
    
    Exit Function
    
ErrHandler:
    StringToUTF8 = strInput
End Function

' Chuyển đổi UTF-8 về Unicode
Public Function UTF8ToString(ByVal strUTF8 As String) As String
    Dim lngLength As Long
    Dim strOutput As String
    
    On Error GoTo ErrHandler
    
    If Len(strUTF8) = 0 Then
        UTF8ToString = ""
        Exit Function
    End If
    
    ' Tính độ dài cần thiết
    lngLength = MultiByteToWideChar(CP_UTF8, 0, strUTF8, -1, vbNullString, 0)
    
    If lngLength > 0 Then
        strOutput = String$(lngLength - 1, vbNullChar)
        MultiByteToWideChar CP_UTF8, 0, strUTF8, -1, strOutput, lngLength
        UTF8ToString = strOutput
    Else
        UTF8ToString = strUTF8
    End If
    
    Exit Function
    
ErrHandler:
    UTF8ToString = strUTF8
End Function

' Kiểm tra string có chứa Unicode không
Public Function HasUnicodeChars(ByVal strInput As String) As Boolean
    Dim i As Long
    Dim lngCharCode As Long
    
    HasUnicodeChars = False
    
    For i = 1 To Len(strInput)
        lngCharCode = AscW(Mid$(strInput, i, 1))
        
        ' Kiểm tra nằm ngoài ASCII (0-127)
        If lngCharCode > 127 Or lngCharCode < 0 Then
            HasUnicodeChars = True
            Exit Function
        End If
    Next i
End Function

' Đếm số ký tự Unicode trong string
Public Function CountUnicodeChars(ByVal strInput As String) As Long
    Dim i As Long
    Dim lngCharCode As Long
    Dim lngCount As Long
    
    lngCount = 0
    
    For i = 1 To Len(strInput)
        lngCharCode = AscW(Mid$(strInput, i, 1))
        
        If lngCharCode > 127 Or lngCharCode < 0 Then
            lngCount = lngCount + 1
        End If
    Next i
    
    CountUnicodeChars = lngCount
End Function

' Lấy danh sách vị trí các ký tự Unicode
Public Function GetUnicodeCharPositions(ByVal strInput As String) As Variant
    Dim positions() As Long
    Dim count As Long
    Dim i As Long
    Dim lngCharCode As Long
    
    count = 0
    ReDim positions(0 To Len(strInput) - 1)
    
    For i = 1 To Len(strInput)
        lngCharCode = AscW(Mid$(strInput, i, 1))
        
        If lngCharCode > 127 Or lngCharCode < 0 Then
            positions(count) = i
            count = count + 1
        End If
    Next i
    
    If count > 0 Then
        ReDim Preserve positions(0 To count - 1)
        GetUnicodeCharPositions = positions
    Else
        GetUnicodeCharPositions = Array()
    End If
End Function

' Chuyển đổi string sang byte array (UTF-8)
Public Function StringToByteArray(ByVal strInput As String) As Byte()
    Dim arrBytes() As Byte
    Dim strUTF8 As String
    
    On Error GoTo ErrHandler
    
    strUTF8 = StringToUTF8(strInput)
    arrBytes = StrConv(strUTF8, vbFromUnicode)
    StringToByteArray = arrBytes
    
    Exit Function
    
ErrHandler:
    ReDim arrBytes(0)
    StringToByteArray = arrBytes
End Function

' Chuyển đổi byte array về string (UTF-8)
Public Function ByteArrayToString(ByRef arrBytes() As Byte) As String
    Dim strTemp As String
    
    On Error GoTo ErrHandler
    
    strTemp = StrConv(arrBytes, vbUnicode)
    ByteArrayToString = UTF8ToString(strTemp)
    
    Exit Function
    
ErrHandler:
    ByteArrayToString = ""
End Function

' ============================================
' VIETNAMESE SPECIFIC FUNCTIONS
' ============================================

' Kiểm tra có phải ký tự tiếng Việt không
Public Function IsVietnameseChar(ByVal char As String) As Boolean
    Dim lngCharCode As Long
    
    IsVietnameseChar = False
    
    If Len(char) = 0 Then Exit Function
    
    lngCharCode = AscW(Left$(char, 1))
    
    ' Unicode ranges cho tiếng Việt:
    ' Latin Extended-A: U+0100 to U+017F (256-383)
    ' Latin Extended-B: U+0180 to U+024F (384-591)
    ' Combining Diacritical Marks: U+0300 to U+036F (768-879)
    
    If (lngCharCode >= 256 And lngCharCode <= 591) Or _
       (lngCharCode >= 768 And lngCharCode <= 879) Or _
       (lngCharCode >= &H1EA0 And lngCharCode <= &H1EF9) Then
        IsVietnameseChar = True
    End If
End Function

' Đếm số ký tự tiếng Việt
Public Function CountVietnameseChars(ByVal strInput As String) As Long
    Dim i As Long
    Dim count As Long
    
    count = 0
    
    For i = 1 To Len(strInput)
        If IsVietnameseChar(Mid$(strInput, i, 1)) Then
            count = count + 1
        End If
    Next i
    
    CountVietnameseChars = count
End Function

' Kiểm tra chuỗi có chứa tiếng Việt không
Public Function HasVietnameseText(ByVal strInput As String) As Boolean
    HasVietnameseText = (CountVietnameseChars(strInput) > 0)
End Function

' ============================================
' TEXT ENCODING DETECTION
' ============================================

' Phát hiện encoding của string
Public Function DetectEncoding(ByVal strInput As String) As String
    Dim hasUnicode As Boolean
    Dim hasVietnamese As Boolean
    
    hasUnicode = HasUnicodeChars(strInput)
    hasVietnamese = HasVietnameseText(strInput)
    
    If hasVietnamese Then
        DetectEncoding = "UTF-8 (Vietnamese)"
    ElseIf hasUnicode Then
        DetectEncoding = "Unicode"
    Else
        DetectEncoding = "ASCII"
    End If
End Function

' ============================================
' FILE I/O WITH UNICODE SUPPORT
' ============================================

' Đọc file text với UTF-8 encoding
Public Function ReadTextFileUTF8(ByVal filePath As String) As String
    Dim stream As Object
    Dim content As String
    
    On Error GoTo ErrHandler
    
    ' Sử dụng ADODB.Stream để đọc UTF-8
    Set stream = CreateObject("ADODB.Stream")
    
    With stream
        .Type = 2 ' adTypeText
        .Charset = "UTF-8"
        .Open
        .LoadFromFile filePath
        content = .ReadText
        .Close
    End With
    
    ReadTextFileUTF8 = content
    
    Exit Function
    
ErrHandler:
    ReadTextFileUTF8 = ""
    If Not stream Is Nothing Then
        On Error Resume Next
        stream.Close
    End If
End Function

' Ghi file text với UTF-8 encoding
Public Function WriteTextFileUTF8(ByVal filePath As String, ByVal content As String) As Boolean
    Dim stream As Object
    
    On Error GoTo ErrHandler
    
    Set stream = CreateObject("ADODB.Stream")
    
    With stream
        .Type = 2 ' adTypeText
        .Charset = "UTF-8"
        .Open
        .WriteText content
        .SaveToFile filePath, 2 ' adSaveCreateOverWrite
        .Close
    End With
    
    WriteTextFileUTF8 = True
    
    Exit Function
    
ErrHandler:
    WriteTextFileUTF8 = False
    If Not stream Is Nothing Then
        On Error Resume Next
        stream.Close
    End If
End Function

' ============================================
' UTILITY FUNCTIONS
' ============================================

' Escape Unicode characters to \uXXXX format
Public Function EscapeUnicode(ByVal strInput As String) As String
    Dim i As Long
    Dim lngCharCode As Long
    Dim strOutput As String
    
    strOutput = ""
    
    For i = 1 To Len(strInput)
        lngCharCode = AscW(Mid$(strInput, i, 1))
        
        If lngCharCode > 127 Or lngCharCode < 0 Then
            strOutput = strOutput & "\u" & Right$("0000" & Hex$(lngCharCode And &HFFFF&), 4)
        Else
            strOutput = strOutput & Mid$(strInput, i, 1)
        End If
    Next i
    
    EscapeUnicode = strOutput
End Function

' Unescape \uXXXX format to Unicode
Public Function UnescapeUnicode(ByVal strInput As String) As String
    Dim i As Long
    Dim strOutput As String
    Dim strHex As String
    Dim lngCharCode As Long
    
    strOutput = ""
    i = 1
    
    Do While i <= Len(strInput)
        If Mid$(strInput, i, 2) = "\u" Then
            ' Lấy 4 ký tự hex
            strHex = Mid$(strInput, i + 2, 4)
            lngCharCode = CLng("&H" & strHex)
            strOutput = strOutput & ChrW$(lngCharCode)
            i = i + 6
        Else
            strOutput = strOutput & Mid$(strInput, i, 1)
            i = i + 1
        End If
    Loop
    
    UnescapeUnicode = strOutput
End Function

' Hiển thị thông tin debug về encoding
Public Sub ShowEncodingInfo(ByVal strInput As String)
    Dim msg As String
    
    msg = "=== THÔNG TIN ENCODING ===" & vbCrLf & vbCrLf
    msg = msg & "Độ dài: " & Len(strInput) & " ký tự" & vbCrLf
    msg = msg & "Số ký tự Unicode: " & CountUnicodeChars(strInput) & vbCrLf
    msg = msg & "Số ký tự tiếng Việt: " & CountVietnameseChars(strInput) & vbCrLf
    msg = msg & "Encoding: " & DetectEncoding(strInput) & vbCrLf & vbCrLf
    msg = msg & "Nội dung (escaped):" & vbCrLf
    msg = msg & EscapeUnicode(strInput)
    
    MsgBox msg, vbInformation, "Encoding Info"
End Sub

' ============================================
' TEST FUNCTION
' ============================================

Public Sub TestUnicodeAPI()
    Dim testString As String
    Dim result As String
    
    testString = "Xin chào! Tiếng Việt có dấu: áàảãạ, đ, ơư"
    
    Debug.Print "Original: " & testString
    Debug.Print "Has Unicode: " & HasUnicodeChars(testString)
    Debug.Print "Unicode Count: " & CountUnicodeChars(testString)
    Debug.Print "Vietnamese Count: " & CountVietnameseChars(testString)
    Debug.Print "Encoding: " & DetectEncoding(testString)
    Debug.Print "Escaped: " & EscapeUnicode(testString)
    
    ShowEncodingInfo testString
End Sub
