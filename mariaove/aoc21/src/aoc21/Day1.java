package aoc21;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Day1 {

	public static ArrayList<String> datos = new ArrayList<String>(); // Create an ArrayList object
	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub

		 File doc = new File("C:\\Users\\ovejerom\\eclipse-workspace\\aoc21\\src\\aoc21\\data\\reto1.txt");
	
		
		        Scanner obj = new Scanner(doc);

		        while (obj.hasNextLine()) {
		        	datos.add(obj.nextLine());
		        }
	}
	
	
	public static void parte1() {
		int aux=0;
		int contador=0;
		for(int i = 1; i<=(datos.size()-1);i++) {
			aux = Integer.parseInt((String) datos.get(i-1));
			
			if(aux< Integer.parseInt((String) datos.get(i))) {
				contador++;
			}
			
		}
		System.out.println(contador);
		
	}
	
	
	public static void parte2(){
		
		ArrayList<String> sumas = new ArrayList<String>();
		for (int i=0; i< (datos.size()-2);i++) {
			int aux = Integer.parseInt((String)datos.get(i))+Integer.parseInt((String)datos.get(i+1))+Integer.parseInt((String)datos.get(i+2));
					sumas.add(Integer.toString(aux));
			
		}
		datos = sumas;
		parte1();
	}
	
	
	
}
