package aoc21;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Day3 {

	
	public static ArrayList<String> datos = new ArrayList<String>(); // Create an ArrayList object
	public static ArrayList<String> datos2 = new ArrayList<String>(); // Create an ArrayList object

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub

		 File doc = new File("C:\\Users\\ovejerom\\eclipse-workspace\\aoc21\\src\\aoc21\\data\\reto3");
	
		        Scanner obj = new Scanner(doc);
		        Scanner obj2 = new Scanner(doc);


		        while (obj.hasNextLine()) {
		        	datos.add(obj.nextLine());
		        	datos2.add(obj2.nextLine());

		        	
		        }
	}
	
	
	
	
	public static int binaryToInteger(String binary) {
	    char[] numbers = binary.toCharArray();
	    int result = 0;
	    for(int i=numbers.length - 1; i>=0; i--)
	        if(numbers[i]=='1')
	            result += Math.pow(2, (numbers.length-i - 1));
	    return result;
	}
	
	public static void parte1() {
		double contadorunos =0;
		double contadorceros =0;
double total = 0;
    	for (int i =0; i<12;i++) {
    		if( consultador(i,datos)>500){
    			//mayoría 1
    			contadorunos = contadorunos + Math.pow(2, (11-i));
    		}else {
    			//mayoría 0
    			contadorceros = contadorceros + Math.pow(2, (11-i));
    		}
    	}
    	total = contadorunos*contadorceros;
    	System.out.println(total);
	}
	
	public static int consultador(int indice, ArrayList datos) {
		int[] posiciones = new int[12];
		for (int i = 0; i< datos.size();i++) {
			String aux = (String) datos.get(i);
			String[] parts = aux.split("");
			
			for (int j=0; j<12;j++) {
				posiciones[j]=(posiciones[j]+Integer.parseInt(parts[j]));
			}
		}
		
		for (int k=0; k<posiciones.length;k++) {
			//System.out.println("resultado "+ k +": "+posiciones[k]);
		}
		return posiciones[indice];
	}
	
	
	public static int parte2_a() {
				
				int posicionbit =0;
				while(datos.size()>1) {
					
					//eliminar posiciones que son minoría
					if((consultador(posicionbit,datos))<((datos.size()-consultador(posicionbit,datos)))){
						
						for(int i=0;i<datos.size();i++) {
							String otro = (String) datos.get(i);
							String[] parts = otro.split("");		
							if(parts[posicionbit].equals("0")) {
								datos.remove(i);
								i--;
							}
						}
					}else {
						for(int i=0;i<datos.size();i++) {
							String segundo = (String) datos.get(i);
							String[] parts = segundo.split("");		
			
							if(parts[posicionbit].equals("1")) {
								datos.remove(i);
								i--;
							}
						}
					}
					posicionbit++;
					if(posicionbit==12) {
						posicionbit=0;
					}
				}
				return(binaryToInteger( datos.get(0)));		
	}
	
	public static int parte2_b() {
		int posicionbit =0;
		while(datos2.size()>1) {
			
			//eliminar posiciones que son minoría
			if((consultador(posicionbit,datos2))>=((datos2.size()-consultador(posicionbit,datos2)))){
				
				for(int i=0;i<datos2.size();i++) {
					String otro = (String) datos2.get(i);
					String[] parts = otro.split("");		
					if(parts[posicionbit].equals("0")) {
						datos2.remove(i);
						i--;
					}
				}
			}else {
				for(int i=0;i<datos2.size();i++) {
					String segundo = (String) datos2.get(i);
					String[] parts = segundo.split("");		
	
					if(parts[posicionbit].equals("1")) {
						datos2.remove(i);
						i--;
					}
				}
			}
			posicionbit++;
			if(posicionbit==12) {
				posicionbit=0;
			}
		}

		return(binaryToInteger( datos2.get(0)));		
}
	
	
	

}
