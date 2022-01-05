package aoc21;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Scanner;



public class Main {

	public static ArrayList<String> datos = new ArrayList<String>(); // Create an ArrayList object
	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub

		 File doc = new File("C:\\Users\\ovejerom\\eclipse-workspace\\aoc21\\src\\aoc21\\data\\reto");
	
		
		        Scanner obj = new Scanner(doc);

		        while (obj.hasNextLine()) {
		        	datos.add(obj.nextLine());
		        }
		  
		        
	  
		        
		        /*
		Day1 day1 = new Day1();
		day1.main(args);
		System.out.println("Resultado día 1 parte 1: ");
		day1.parte1();
		System.out.println("Resultado día 1 parte 2: ");
		day1.parte2();
		*/  
		       /*
		Day2 day2 = new Day2();
		day2.main(args);
		System.out.println("Resultado día 2 parte 1: ");
		day2.parte1();
		System.out.println("Resultado día 2 parte 2: ");
		day2.parte2();		        
	    */	
		        /*
		Day3 day3 = new Day3();
		day3.main(args);
		System.out.println("Resultado día 3 parte 1: ");
		day3.parte1();
		System.out.println("Resultado día 3 parte 2: ");
		System.out.println(day3.parte2_a()*day3.parte2_b());		
		*/
		        
		    /*    
		Day5 day5 = new Day5();
		System.out.println("Resultado día 5: ");
		day5.main(args);
		   */
		        
		
					
	}

	
	
	

	
	
		
	
	
	

}
