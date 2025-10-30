Option Explicit

' ===========================
' USERFORM: frmTextCleaner
' Mô tả: Form giao diện cho Text Cleaner với Unicode support
' ===========================

' Windows API cho Unicode display
Private Declare PtrSafe Function SendMessageW Lib "user32" ( _
    ByVal hWnd As LongPtr, _
    ByVal wMsg As Long, _
    ByVal wParam As LongPtr, _
    ByVal lParam As LongPtr) As LongPtr

Private Const WM_SETTEXT = &HC

' Biến local
Private m_PreviewMode As Boolean
Private m_ProcessStartTime As Double

' ===========================
' FORM EVENTS
' ===========================

Private Sub UserForm_Initialize()
    ' Thiết lập giao diện ban đầu
    Me.Caption = ConvertToUnicode("Công cụ dọn dẹp Text - Xóa dòng tiếng Anh")
    
    ' Set labels với Unicode
    lblTitle.Caption = ConvertToUnicode("CÔNG CỤ XÓA DÒNG TIẾNG ANH")
    lblDescription.Caption = ConvertToUnicode("Công cụ này sẽ xóa các dòng chỉ chứa ký tự ASCII (tiếng Anh)" & vbCrLf & _
                                               "và giữ lại các dòng có ký tự Unicode (tiếng Việt)")
    
    lblOptions.Caption = ConvertToUnicode("TÙY CHỌN XỬ LÝ:")
    chkPreview.Caption = ConvertToUnicode("Xem trước kết quả (Preview)")
    chkBackup.Caption = ConvertToUnicode("Tạo backup để có thể Undo")
    chkShowStats.Caption = ConvertToUnicode("Hiển thị thống kê chi tiết")
    
    lblProgress.Caption = ConvertToUnicode("Trạng thái: Chưa xử lý")
    
    btnProcess.Caption = ConvertToUnicode("Bắt đầu xử lý")
    btnUndo.Caption = ConvertToUnicode("Hoàn tác (Undo)")
    btnClose.Caption = ConvertToUnicode("Đóng")
    btnHelp.Caption = ConvertToUnicode("Trợ giúp")
    
    ' Default settings
    chkPreview.Value = True
    chkBackup.Value = True
    chkShowStats.Value = True
    
    btnUndo.Enabled = False
    
    ' Clear preview
    txtPreview.Text = ""
    txtPreview.Visible = False
    lblPreviewTitle.Visible = False
    
    ' Reset progress
    progressBar.Width = 0
    
    ' Reset stats
    lblStats.Caption = ""
End Sub

' ===========================
' BUTTON EVENTS
' ===========================

Private Sub btnProcess_Click()
    Dim startTime As Double
    Dim actions() As ActionItem
    Dim actionCount As Long
    
    On Error GoTo ErrHandler
    
    startTime = Timer
    m_ProcessStartTime = startTime
    
    ' Disable buttons
    btnProcess.Enabled = False
    btnClose.Enabled = False
    
    UpdateStatus "Đang quét presentation..."
    DoEvents
    
    ' Thu thập actions
    CollectAllActions actions, actionCount
    
    If actionCount = 0 Then
        UpdateStatus "Không tìm thấy textbox nào cần xử lý"
        MsgBox ConvertToUnicode("Không tìm thấy textbox nào cần xử lý."), vbInformation
        GoTo ExitPoint
    End If
    
    ' Lưu preview actions
    g_PreviewCount = actionCount
    ReDim g_PreviewActions(0 To actionCount - 1)
    Dim i As Long
    For i = 0 To actionCount - 1
        g_PreviewActions(i) = actions(i)
    Next i
    
    ' Preview mode
    If chkPreview.Value Then
        ShowPreview actions, actionCount
        
        Dim response As VbMsgBoxResult
        response = MsgBox(ConvertToUnicode("Bạn có muốn tiếp tục xử lý?"), vbYesNo + vbQuestion, "Xác nhận")
        
        If response = vbNo Then
            UpdateStatus "Đã hủy xử lý"
            GoTo ExitPoint
        End If
    End If
    
    ' Thực hiện xử lý
    UpdateStatus "Đang xử lý..."
    UpdateProgress 50
    DoEvents
    
    PerformActions actions, actionCount
    
    UpdateProgress 100
    g_Stats.ProcessingTime = Timer - startTime
    
    ' Hiển thị kết quả
    UpdateStatus "Hoàn tất!"
    
    If chkShowStats.Value Then
        ShowStatistics
    End If
    
    If chkBackup.Value Then
        btnUndo.Enabled = True
    End If
    
    MsgBox ConvertToUnicode("Xử lý hoàn tất!" & vbCrLf & _
                            "Đã sửa: " & g_Stats.ShapesModified & " textbox" & vbCrLf & _
                            "Đã xóa: " & g_Stats.ShapesDeleted & " textbox"), _
           vbInformation, "Thành công"

ExitPoint:
    btnProcess.Enabled = True
    btnClose.Enabled = True
    Exit Sub

ErrHandler:
    MsgBox ConvertToUnicode("Lỗi: " & Err.Description), vbExclamation
    Resume ExitPoint
End Sub

Private Sub btnUndo_Click()
    Dim response As VbMsgBoxResult
    
    If g_UndoCount = 0 Then
        MsgBox ConvertToUnicode("Không có thao tác nào để hoàn tác."), vbInformation
        Exit Sub
    End If
    
    response = MsgBox(ConvertToUnicode("Bạn có chắc muốn hoàn tác " & g_UndoCount & " thay đổi?" & vbCrLf & _
                                        "Lưu ý: Không thể khôi phục các shape đã bị xóa."), _
                      vbYesNo + vbQuestion, "Xác nhận Undo")
    
    If response = vbYes Then
        UpdateStatus "Đang hoàn tác..."
        DoEvents
        
        PerformUndo
        
        UpdateStatus "Đã hoàn tác thành công"
        btnUndo.Enabled = False
        UpdateProgress 0
        lblStats.Caption = ""
        
        MsgBox ConvertToUnicode("Đã hoàn tác thành công!"), vbInformation
    End If
End Sub

Private Sub btnClose_Click()
    Unload Me
End Sub

Private Sub btnHelp_Click()
    Dim helpMsg As String
    
    helpMsg = "=== HƯỚNG DẪN SỬ DỤNG ===" & vbCrLf & vbCrLf
    helpMsg = helpMsg & "1. Chọn các tùy chọn phù hợp:" & vbCrLf
    helpMsg = helpMsg & "   - Preview: Xem trước kết quả" & vbCrLf
    helpMsg = helpMsg & "   - Backup: Cho phép Undo" & vbCrLf
    helpMsg = helpMsg & "   - Thống kê: Hiển thị báo cáo chi tiết" & vbCrLf & vbCrLf
    helpMsg = helpMsg & "2. Nhấn 'Bắt đầu xử lý'" & vbCrLf & vbCrLf
    helpMsg = helpMsg & "3. Nếu cần hoàn tác, nhấn 'Hoàn tác (Undo)'" & vbCrLf & vbCrLf
    helpMsg = helpMsg & "=== QUY TẮC XỬ LÝ ===" & vbCrLf & vbCrLf
    helpMsg = helpMsg & "- Giữ lại: Dòng có ít nhất 1 ký tự Unicode" & vbCrLf
    helpMsg = helpMsg & "  (tiếng Việt có dấu, emoji, v.v.)" & vbCrLf & vbCrLf
    helpMsg = helpMsg & "- Xóa: Dòng chỉ chứa ký tự ASCII" & vbCrLf
    helpMsg = helpMsg & "  (tiếng Anh, số, ký tự đặc biệt cơ bản)" & vbCrLf & vbCrLf
    helpMsg = helpMsg & "- Nếu textbox rỗng sau khi lọc → Xóa luôn textbox"
    
    MsgBox ConvertToUnicode(helpMsg), vbInformation, "Trợ giúp"
End Sub

Private Sub chkPreview_Click()
    If chkPreview.Value Then
        txtPreview.Visible = False
        lblPreviewTitle.Visible = False
    End If
End Sub

' ===========================
' UI HELPER FUNCTIONS
' ===========================

Private Sub UpdateStatus(ByVal msg As String)
    lblProgress.Caption = ConvertToUnicode("Trạng thái: " & msg)
    DoEvents
End Sub

Private Sub UpdateProgress(ByVal percent As Long)
    If percent < 0 Then percent = 0
    If percent > 100 Then percent = 100
    
    progressBar.Width = (frameProgress.Width - 4) * percent / 100
    DoEvents
End Sub

Private Sub ShowPreview(ByRef actions() As ActionItem, ByVal actionCount As Long)
    Dim previewText As String
    Dim i As Long
    Dim maxItems As Long
    
    maxItems = 20
    
    previewText = "Tìm thấy " & actionCount & " thay đổi:" & vbCrLf & vbCrLf
    
    For i = 0 To IIf(actionCount > maxItems, maxItems - 1, actionCount - 1)
        previewText = previewText & "[Slide " & actions(i).SlideIndex & "] "
        previewText = previewText & actions(i).ShapeName & ": "
        
        If actions(i).DeleteShape Then
            previewText = previewText & "XÓA" & vbCrLf
        Else
            previewText = previewText & "CẬP NHẬT" & vbCrLf
            previewText = previewText & "  Trước: " & Left(Replace(actions(i).OriginalText, vbCrLf, " "), 40) & "..." & vbCrLf
            previewText = previewText & "  Sau:  " & Left(Replace(actions(i).NewText, vbCrLf, " "), 40) & "..." & vbCrLf
        End If
        previewText = previewText & vbCrLf
    Next i
    
    If actionCount > maxItems Then
        previewText = previewText & "... và " & (actionCount - maxItems) & " thay đổi khác"
    End If
    
    lblPreviewTitle.Visible = True
    lblPreviewTitle.Caption = ConvertToUnicode("=== XEM TRƯỚC KẾT QUẢ ===")
    txtPreview.Visible = True
    txtPreview.Text = ConvertToUnicode(previewText)
    
    ' Resize form nếu cần
    If Me.Height < 500 Then
        Me.Height = 500
    End If
End Sub

Private Sub ShowStatistics()
    Dim statsText As String
    
    statsText = "=== THỐNG KÊ XỬ LÝ ===" & vbCrLf & vbCrLf
    statsText = statsText & "Tổng số slide: " & FormatNumber(g_Stats.TotalSlides) & vbCrLf
    statsText = statsText & "Tổng số shape: " & FormatNumber(g_Stats.TotalShapes) & vbCrLf
    statsText = statsText & "Shape đã sửa: " & FormatNumber(g_Stats.ShapesModified) & vbCrLf
    statsText = statsText & "Shape đã xóa: " & FormatNumber(g_Stats.ShapesDeleted) & vbCrLf
    statsText = statsText & vbCrLf
    statsText = statsText & "Dòng đã xóa: " & FormatNumber(g_Stats.LinesRemoved) & vbCrLf
    statsText = statsText & "Dòng đã giữ: " & FormatNumber(g_Stats.LinesKept) & vbCrLf
    statsText = statsText & vbCrLf
    statsText = statsText & "Thời gian: " & FormatTime(g_Stats.ProcessingTime)
    
    lblStats.Caption = ConvertToUnicode(statsText)
End Sub

' ===========================
' UNICODE SUPPORT FUNCTIONS
' ===========================

Private Function ConvertToUnicode(ByVal text As String) As String
    ' VBA hỗ trợ Unicode tốt, chỉ cần ensure encoding
    ConvertToUnicode = text
End Function

' Set text cho control với Unicode
Private Sub SetControlTextUnicode(ByVal ctrl As Control, ByVal text As String)
    On Error Resume Next
    
    ' VBA UserForm controls hỗ trợ Unicode natively
    ctrl.Caption = text
    
    On Error GoTo 0
End Sub
