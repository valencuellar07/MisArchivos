using System;
public class Program{

  //Ejercicio de codewars
	
  const int POWER_BASE=2;
	
  public static void Main() {
        // Display the number of command line arguments.
        Console.WriteLine("Numero de 1s en el binario: "+CountBits(29));
    }
  
  public static int CountBits(int decimalInput){
    bool stop = false;
    int power = 0;
    int counter = 0;
    do{
      power = (int)Math.Pow(POWER_BASE, counter); 
      counter++;
      if(power > decimalInput){
        stop=true;
      }
    }while (stop==false);
    
    return OnesCounter(counter, decimalInput);
  }
  
  public static int OnesCounter(int counter, int decimalInput){
    int minus = 0;
    int countOnes = 0;
    int plus = 0;
	  
    for (int index = counter-1; index > -1; index--){
	  
      int currentPower = (int)Math.Pow(POWER_BASE, index);
		
      if(index == counter-1){
	minus = decimalInput;
      }
      if(minus < currentPower){
        continue;
      }
      else{
	  plus += currentPower;
	  minus = decimalInput - plus;
	  countOnes+=1;
      }	
      if(plus == decimalInput){
        break;
      }   
    }
     return countOnes;
  }
}
