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

from validate import ValidateCLIArgs, ValidateResult, ValidatePinpointWrapper

def Validate(args: ValidateCLIArgs.CliArgs) -> ValidateResult.ValidateResult:
  # validate args
  valid, err = args.validate()

  #check arg validity
  if valid:
    #create a pinpoint wrapper
    wrapper = ValidatePinpointWrapper.ValidatePinpointWrapper()
    
    #create a validate result configuration
    ValidateResultCfg = args.validateResultConfig()
    
    #create a new validate result object
    result = ValidateResult.ValidateResult(ValidateResultCfg)
    
    #for each phone number validate request
    for NumberValidateRequest in args.PhoneNumberValidateRequests():
      
      #validate the phone number
      NumberValidateResponse = wrapper.PhoneNumberValidate(NumberValidateReqeust=NumberValidateRequest)
      
      #extract the response
      NumberValidateResponse = NumberValidateResponse['NumberValidateResponse'] if 'NumberValidateResponse' in NumberValidateResponse else None
      
      #add response if not None
      if NumberValidateResponse is not None:
        result.Add(NumberValidateResponse)
    
    return result
  else:
    #failed to validate args
    raise ValueError(f"invalid args: {err}")