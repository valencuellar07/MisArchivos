using System;
using System.Collections.Generic;
using System.Text;

//Ejercicio de CodeWars
// Dictionary CHAR_TO_MORSE in the class Preloaded is already defined to convert characters into their Morse Code equivilant.
public class MorseEncrypt
{
  public static StringBuilder ToMorse(string englishStr)
  {
    List<char> letters = new List<char>();
    letters.AddRange(englishStr);
    StringBuilder morseCode = new StringBuilder();
    
    foreach (char currentLetter in letters){
      
      if(currentLetter!=' '){
        morseCode.Append(Preloaded.CHAR_TO_MORSE[char.ToUpper(currentLetter)]);
        morseCode.Append(" ");
      }
      else{
        morseCode.Append("  ");
      }
      
    }
    
    //Console.Write(Preloaded.CHAR_TO_MORSE);
    
    return morseCode;
  }
  
  
  
}
