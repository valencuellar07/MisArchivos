using System;
using System.Text;
					
public class Program {
	
	public static void Main() {
				
		String stringChain = null;
		bool repeatWhile= true;	
		do 
		{   
			repeatWhile= true;
		  	Console.WriteLine("Escribe la cadena que deseas comprimir:");
			stringChain = Console.ReadLine();
			if(ValidateInputHasNumbers(stringChain)==false && ValidateInputLength(stringChain)==false){ //if the input doesn't have numbers and length is less than 256 characters, 
				repeatWhile=false;                                                                   //exit while and continue to the next function
			}
		}
		while (repeatWhile == true);
		
		WriteChain(CompareStrings(stringChain,CompressString(stringChain)));
	}
	
	public const int MAX_CHARACTERS=256;
	
	public static bool ValidateInputHasNumbers (String stringChain){ // validates if the input has numbers
		
		bool hasNumber = false;
		for(int i=0; i<stringChain.Length;i++ ){
           if(Char.IsNumber(stringChain[i])){
			   hasNumber=true;
			   Console.WriteLine("¡Error! Escribiste una cadena con números incluidos.");
			   break;
		   }
        }
		return hasNumber;
	}
	
	public static bool ValidateInputLength(String stringChain){
		
		bool exceedsMaximum = false;
		if(stringChain.Length>MAX_CHARACTERS){
			Console.WriteLine("¡Error! Escribiste una cadena con más de 256 carácteres.");
			exceedsMaximum=true;
		}
		return exceedsMaximum;
	}
	
	public static String CompressString (String stringChain){ // counts letters and concatenates letters and numbers to make the "compression"
		int counter=0;
		StringBuilder compressedChain = new StringBuilder();
		char firstChar = stringChain[0];
		
		foreach (char indexChar in stringChain){ 
			if (!indexChar.Equals(firstChar)){
				compressedChain.Append(firstChar);
				compressedChain.Append(counter.ToString());
				firstChar = indexChar;
				counter=0;
			}
			counter++;
		
        }
		compressedChain.Append(firstChar);
		compressedChain.Append(counter.ToString());
		
		return compressedChain.ToString();
	}
	
	public static string CompareStrings (String stringChain, String compressedChain){
			
		if(compressedChain.Length>stringChain.Length){
			compressedChain=stringChain;
		}
		return compressedChain;
	} 
	
	public static void WriteChain (string chosenString){
		Console.WriteLine(chosenString);
	}
		
	
}