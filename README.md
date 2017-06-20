# Proyecto-Kschool-Basket

This readme try to explain how the content must be work in the linux virtual machine given by Kschool.

There are two python notebook to run. 
1-. web_scrapping_final
2-. proyecto_final

The web_scrapping_final output it is different from the input that the proyecto_final needs. This is why we are not control
the case that the web page structure change. If you want to test the overall process you need to rename the temporadas.csv
to temporadas_old.csv and rename temporadas_web.csv llike temporadas.csv.

The temporadas csv need to be in the same path that notebooks are due there are no paths included in the python call.

Para procesar en linux y en la máquina virtual del curso solo es necesario ejecutar los notebooks:

1-. web_scrapping_final
2-. proyecto_final

El notebook de webscrapping da como salida un fichero que se llama tempordas_web.csv pero este no es el fichero al 
que llama el notebook proyecto_final. Lo hago para que si la web cambia su estructura programa siga funcionando.

EL fichero temporadas.csv que llama proyecto_final tiene que estar situado en la misma carpeta
que el programa puesto que está llamado sin ruta.

