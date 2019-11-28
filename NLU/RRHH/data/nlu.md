## intent:greet
- hey
- hello
- hola
- hola que tal
- buenos dias
- buenas tardes
- buenas noches
- hola buenas

## intent:fine_ask
- bien gracias, como estas?
- bien y tu?
- muy bien, que tal tu?
- todo bien, tu que tal?
- estupendo, y tu?

## intent:fine_normal
- todo bien, gracias
- muy bien
- super bien
- estupendo
- bien
- todo en orden

## intent:set_vacations
- quiero registrar mis vacaciones
- registrar dias libres
- quiero pedirme vacaciones
- pedir periodo vacacional
- quiero pedirme un dia libre
- quisiera pedir dias libres
- quiero pedir dias a cuenta de vacaciones
- quiero pedir vacaciones
- registrar vacaciones
- quiero dias de vacaciones

## intent:get_vacations_available
- cuantos dias de vacaciones me quedan?
- quiero saber cuantos dias libres tengo
- cuantos dias tengo?
- cuantos dias libres tengo?
- dime mis dias de vacaciones
- cuantas vacaciones disponibles tengo
- aún tengo vacaciones? 
- me quedan días disponibles?
- cuantos días libres me quedan?
- quiero saber mis vacaciones

## intent:get_nomina
- dame mi nómina
- dame la nomina de este mes
- muestrame la nomina del mes pasado
- muestra la nomina de los ultimos dos meses
- dame la nómina de hace 3 meses
- enseñame mis nominas desde junio
- dame las nominas de mayo
- dame la nómina de octubre 
- quiero la nómina de enero a diciembre
- quiero mi nómina

## intent:set_schedule_in
- quiero registrar mi entrada
- quiero registrar mi hora de entrada
- quiero registrar la hora de entrada de ayer
- marcar mi entrada
- checar la entrada del lunes
- entro

## intent:set_schedule_out
- quiero registrar mi salida
- quiero registrar mi hora de salida
- quiero registrar la hora de salida de ayer
- marcar mi salida
- checar la salida del lunes
- salgo

## intent:get_schedule_in
- a que hora he entrado?
- cuando registre mi entrada?
- dime mi hora de entrada
- dame la hora de entrada
- cuando entré?
- a que hora entré

## intent:get_schedule_out
- a que hora he salido?
- cuando registre mi salida?
- dime mi hora de salida
- dame la hora de salida
- cuando salí?
- a que hora salí?

## intent:thanks
- gracias
- muchas gracias

## intent:bye
- No, es todo por ahora, bye
- Bye
- adios
- hasta luego
- ciao
- adeu

## intent:affirmative
- si
- si por favor
- correcto
- si, gracias
- afirmativo
- asi es
- eso es

## intent:negation
- no
- no gracias
- incorrecto
- negativo
- no no

## intent:user_number
- mi numero de empleado es [12707315K](id_code)
- mi id es [2348713Y](id_code)
- ok [73498315F](id_code)
- [62592345G](id_code)
- mi numero de usuario es [H4765413H](id_code)

## intent:vacation_range
- del 3 de octubre al 4 de noviembre
- de 3 al 15 de junio
- todo el mes de agosto
- el proximo lunes
- el 17 de diciembre
- pasado mañana
- el jueves que viene
- quiero pedirme el jueves
- quiero vacaciones del 3 al 5 de diciembre
- quiero vacaciones el lunes
- quiero pedirme el lunes

## intent:password_reset
- no recuerdo la contraseña de mi email
- quiero cambiar la contraseña de mi correo
- resetear password de correo
- como cambiar la contraseña de mi correo
- cambiar el password
- problema con el password
- no puedo iniciar sesion en correo
- cambiar contraseña de password

## intent:simple_appointment
- quiero una cita
- agenda una cita
- pideme una cita 
- solicita una cita
- quiero solicitar una cita 
- cita 
- quiero agendar un cita
- quiero obtener una cita 
- pon una cita
- quiero agendar una cita para el 25 de julio
- cita para el 3 de enero
- agenda una cita para el 25 de diciembre
- pide una cita para el 23 de agosto
- quiero una cita para mañana

## intent:category_appointment
- por la mañana
- durante la mañana
- mañana
- en la mañana 
- por la tarde 
- durante la tarde
- en la tarde 
- a medio dia
- durante el medio dia
- medio dia
- tarde

## intent:appointment_with_category
- quiero una cita por la mañana
- agenda una cita por la tarde
- pideme una cita al medio dia
- solicita una cita durante la mañana
- quiero solicitar una cita mañana por la tarde
- cita el 3 de enero por la mañana
- quiero agendar un cita mañana 
- quiero obtener una cita para el jueves por la tarde
- pon una cita para el lunes a medio dia
- quiero agendar una cita para el 25 de julio a medio dia
- cita para el 3 de enero por la mañana
- agenda una cita para el 25 de diciembre por la tarde
- pide una cita para el 23 de agosto por la mañana

## intent:appointment_with_hour
- quiero una cita a las 12
- agenda una cita a las 3 de la tarde
- pideme una cita a las 5 de la tarde
- solicita una cita a las 10 de la mañana
- quiero solicitar una cita mañana a las 17 hrs
- cita el 3 de enero a las 10:00 
- quiero agendar un cita mañana a las 18 hrs 
- quiero obtener una cita para el jueves a las 6 tarde
- pon una cita para el lunes a las 12:00
- quiero agendar una cita para el 25 de julio a las 9

## intent:get_availability
- dime la disponibilidad esta mañana
- que horas hay disponibles para hoy
- hay diponibilidad para el 12 de agosto?
- que disponibilidad hay el miercoles
- durante la tarde que horas hay disponibles
- que horarios hay para el lunes

## intent:spec_hour
- a las 12
- a la 5
- a las 17hrs
- a las 3 de la tarde
- a las 5 de la tarde
- 5 de la tade
- a las 8 de la mañana
- a las 8hrs
- a las 17:00
- a las 10:00
- a las 09:00
- 15 hrs
- 08:00 hrs
- 9 hrs
- 10am
- 11 am

## regex:id_code
- ([a-z]|[A-Z]|[0-9])[0-9]{7}([a-z]|[A-Z]|[0-9])