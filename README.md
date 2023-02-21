# SA_Practica3

## Integrantes
| Coordinador | Nombre | Carné | % de trabajo | 
|-------------|--------|-------|--------------|
| X | Juan Antonio Solares Samayoa | 201800496 | 25% |
|  | Erick José André Villatoro Revolorio | 201900907 | 25% |
|  | Juan Diego Alvarado Salguero  | 201807335 | 25% |
|  | Christofer William Borrayo López | 201602719 | 25% |

## Antecedentes
Debido a la gran afluencia de personas y a la gran cantidad de personas que realizan una fila para solicitar un boleto de una película, la empresa de cines CuevanaLive ha decidido invertir en la creación de un portal web que permita la compra de boletos en línea. 

Pensando siempre en la comodidad del usuario, la empresa CuevanaLive solicita que el portal permita al usuario iniciar sesión en el sistema para poder ver qué películas están en cartelera así como los horarios de estas para luego poder reservar uno o más asientos y posteriormente pagar por estos en línea utilizando una tarjeta de crédito y recibir por correo los boletos comprados.

Aprovechando la nueva implementación, la empresa CuevanaLive ha decidido que integrará un sistema único de membresía mensual llamada CuevanaPlus que permitirá un 10% de descuento en la compra de boletos por medio del portal web para así incentivar a los usuarios a utilizar la página y evitar atascos en las colas físicas del cine. 

CuevanaLive también solicita que se recopile información de los usuarios, específicamente las películas más vistas, los usuarios que más han visitado el cine y los géneros más vistos, etc. para poder luego en un futuro centrar sus esfuerzos administrativos en estos.


## Solución Planteada
Debido a la solicitud de distintas características diferentes dentro del sistema como la compra de boletos, la visualización de cartelera, los servicios de membresía, etc. Se ha optado como grupo desarrollador a una solución basada en microservicios. 

Se realizarán un total de 7 módulos los cuales serán:
* Módulo de usuario: Encargado del manejo de la información y registro de usuarios.

* Módulo de autenticación: Encargado del manejo de la autenticación del usuario.

* Módulo de compra: Encargado del manejo de compra de boletos y membresías

* Módulo de tarjeta: Encargado del manejo de la información de la tarjeta de crédito del usuario

* Módulo de salas: Encargado del manejo de la información relacionada con las salas con las que cuenta una sucursal de cine.

* Módulo de películas: Encargado de la gestión (crear, borrar, editar) de las películas que van a presentarse en cartelera.

* Módulo de datos: Encargado de mostrar datos específicos para posteriormente ser transformados en gráficas en una sección de repostería que serán útiles para poder determinar el funcionamiento de determinadas métricas en el modelo de negocio.

Estos módulos poseen a su vez múltiples funcionalidades que se especifican a continuación a más detalle. 

Todos estos servicios estarán enlazados a una base de datos en la nube y serán accesibles por medio de un proxy para mayor seguridad, agilizar las solicitudes, restringir el acceso y redistribuir la carga de una forma más fácil si en algún momento se llega a optar por la implementación de tecnologías de replicación de servicios como lo son kubernetes.


