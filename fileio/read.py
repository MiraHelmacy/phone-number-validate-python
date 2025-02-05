"""
The MIT License (MIT)

Copyright © 2025 Alex Helmacy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
__MAX_FILE_SIZE = 10 * 1024

def ReadFromFile(filePath: str) -> str:
  #with cfg file open
  with __openFile(filePath) as file:
    
    #files contents
    contents = ""
    
    #for each phone number
    for phoneNumber in file:
      
      #add the phone number to the contents
      contents += phoneNumber

      #check if the contents is bigger than the max file size
      if len(contents) > __MAX_FILE_SIZE:
        raise Exception(f"file too big. max file size: {__MAX_FILE_SIZE}. current size: {len(contents)}")
    
    return contents

def __openFile(filePath: str):
  return open(filePath, 'r')