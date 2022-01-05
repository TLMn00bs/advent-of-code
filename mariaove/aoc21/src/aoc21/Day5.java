package aoc21;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Day5 {

	
	
	public static ArrayList<String> datos = new ArrayList<String>(); // Create an ArrayList object

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub

		 File doc = new File("C:\\Users\\ovejerom\\eclipse-workspace\\aoc21\\src\\aoc21\\data\\reto6");
	
		        Scanner obj = new Scanner(doc);

		        while (obj.hasNextLine()) {
		        	datos.add(obj.nextLine());

		        	
		        }
	
	
	
	int [][] m = new int[1000][1000];
	int [][] parte1 = new int[1000][1000];
	//rellenar todo con 0s
	for(int a =0;  a<1000;a++) {
		for(int b = 0;b<1000;b++ ) {
			m[a][b]=0;
		}
	}
	
	
	
	for (int i =0; i< datos.size();i++) {
		//extraer coordenadas de cada fila de datos
	
		String aux = (String) ((String) datos.get(i)).replace(" ","");
		String[] parts = (aux.split("->"));	
		String[] origen = parts[0].split(",");
		String[] destino = parts[1].split(",");
		String o1 = origen[0];
		String o2 = origen[1];

		String d1 = destino[0];
		String d2 = destino[1];
		int x1 = Integer.parseInt(o1);
		int y1 = Integer.parseInt(o2);
		int x2 = Integer.parseInt(d1);
		int y2 = Integer.parseInt(d2);

	//comprobar si es una línea vertical, horizontal o diagonal 
		
		if(x1==x2) { //línea vertical detectada
			
			if(y1<y2) { //hacia que sentido va la línea?
				for(int j=y1;j<=y2;j++) {
					m[x1][j] = m[x1][j]+1;
					parte1[x1][j] = parte1[x1][j]+1;

					//System.out.println("vertical "+x1+"   "+j);
				}
			}else {
				for(int j=y2;j<=y1;j++) {
					m[x1][j] = m[x1][j]+1;
					parte1[x1][j] = parte1[x1][j]+1;

					//System.out.println("vertical "+x1+"   "+j);
				}	
			}
		}
		
		if(y1==y2) { //línea horizontal
			
			if(x1<x2) { //hacia que sentido va la linea?
				for(int j=x1;j<=x2;j++) {
					m[j][y1] = m[j][y1]+1;
					parte1[j][y1] = parte1[j][y1]+1;

				}
			}else{
				for(int j=x2;j<=x1;j++) {
					m[j][y1] = m[j][y1]+1;	
					parte1[j][y1] = parte1[j][y1]+1;	

				}	
			}
		}
		
		if(Math.abs(x2-x1)==Math.abs(y2-y1)) {//detectada diagonallllllll
			//System.out.println("diagonal  "+x1+"   "+y1+"   "+x2+"   "+y2);
			
			for (int k = 0; k<= Math.abs(x2-x1);k++) {
				
				if((x1<x2) &&(y1<y2)) {
					m[x1+k][y1+k]= m[x1+k][y1+k]+1;	
				}
				if((x1<x2) &&(y1>y2)) {
					m[x1+k][y1-k]= m[x1+k][y1-k]+1;	
				}
				if((x1>x2) &&(y1<y2)) {
					m[x1-k][y1+k]= m[x1-k][y1+k]+1;	
				//	System.out.println("tres "+ (x1-k)+"    "+ (y1+k));
				}
				if((x1>x2) &&(y1>y2)) {
					m[x1-k][y1-k]= m[x1-k][y1-k]+1;	
				//System.out.println("cuatro");
				}
			}	
		}	
	}
	
	int resultado=0;
	int resultadoparte1=0;
	for(int a =0;  a<1000;a++) {
		for(int b = 0;b<1000;b++ ) {
			if(m[a][b]>=2) {
				resultado++;
				//System.out.println("posicion: "+a+"   "+b);
			}
			if(parte1[a][b]>=2) {
				resultadoparte1++;
				//System.out.println("posicion: "+a+"   "+b);
			}
		}
	}
	System.out.println("Parte 1: "+ resultadoparte1);
	System.out.println("Parte 2: "+resultado);
	
	
	
	}
	
}
