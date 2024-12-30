import sqlite3
import os

conn = sqlite3.connect("clinic_database2.db")
c = conn.cursor()



while True:
    print("\nΠατήστε Q για νέα αναζήτηση.")
    print("Πατήστε N για εισαγωγή νέου ραντεβού.")
    print("Πατήστε 0 για έξοδο.")
    action = input("\nEπιλέξτε ενέργεια:")
#########################ΕΡΩΤΗΣΕΙΣ##############################################################################################
    if action == "Q":
        print("Ερώτηση 1: Πόσα παιδιά έχουν κλείσει ραντεβού στην κλινική;")
        print("Ερώτηση 2: Πόσα ραντεβού έχει εκτελέσει ο κάθε γιατρός μέχρι το 2023;")
        print("Ερώτηση 3: Ποιος είναι ο μέσος όρος διαρκειάς ραντεβού για ασθενής πάνω απο 65 για κάθε γιατρό;")
        print("Ερώτηση 4: Ποιες 5 ειδικότητες επισκέφτηκαν περισσότερο οι γυναίκες το 2019;")
        print("Ερώτημα 5: Ποιος ασθενής ακύρωσε τα περισσότερα ραντεβού που είχε προγραμματίσει για το 2023;")
        print("Ερώτημα 6: Τι ώρα ξεκινάνε τα περισσότερα ραντεβού ενός γιατρού;")
        print("Ερώτημα 7: Ποιους γιατρούς έχει επισκεφτεί ένας ασθενής;")
        print("Ερώτημα 8: Ποιοι γιατροί δεν δούλευαν στις 30/8/2020;")
        print("Ερώτημα 9: Δείτε όλους τους γιατρούς μιας ειδικότητας.")
        print("Ερώτημα 10: Δείτε τους ασθενείς που έχουν επισκεφτεί κάποιον γιατρό.")
        print("Ερώτημα 11: Δείτε τα προγραμματισμένα ραντεβού ενός γιατρού.")
        print("Ερώτημα 12: Δείτε τα ακυρωμένα ραντεβού ενός γιατρού.")
        print("Ερώτημα 13: Δείτε τις μέρες που δεν δουλεύει στην κλινική ένας γιατρός για κάποιο έτος.")


        print("Πατήστε 0 για να πάτε πίσω.")

        while True:
            query = input("\nΕπιλέξτε ερώτημα:")
            if query == "0":
                print("Πίσω στην αρχική...")
                break
            elif query == "1":
                ##Query 1: Ασθενείς κάτω των 18
                print("Ερώτηση 1: Πόσα παιδιά έχουν κλείσει ραντεβού στην κλινική;")
                c.execute(" select count(*) from Patient where age < 18")
                data = c.fetchall()
                for t in data:
                    print("Το νοσοκομειο εξυπηρέτησε", t[0], "παιδιά.\n")

            elif query == "2":
                ##Query 2:Αριθμός συνολικών ραντεβού κάθε γιατρού μέχρι το 2023
                print("Ερώτηση 2: Πόσα ραντεβού έχει εκτελέσει ο κάθε γιατρός μέχρι το 2023;")
                c.execute("select c.doctor_id, d.lastname, d.speciality,count(*)\
                            from doctor as d, choice as c\
                            where c.doctor_id = d.doctor_id and c.year<2023 and \
                            c.app_state = 'EXECUTED'\
                            group by c.doctor_id \
                            order by count(*)")
                data = c.fetchall()
                style = "{:<10}	 {:<10}	 {:<15}	 {:<10}"
                print(style.format("ID","ΓΙΑΤΡΟΣ", "ΕΙΔΙΚΟΤΗΤΑ", "ΑΡΙΘΜΟΣ ΡΑΝΤΕΒΟΥ"))
                for t in data:
                    print( style.format(t[0],t[1],t[2],t[3]))

            elif query == "3":
                #:Query 3: Μέσος όρος διάρκειας ραντεβού για ασθενείς πάνω από 65 ανά γιατρό
                print("\nΕρώτηση 3: Ποιος είναι ο μέσος όρος διαρκειάς ραντεβού για ασθενής πάνω απο 65 για κάθε γιατρό;")
                c.execute("select d.doctor_id, d.lastname ,avg(c.duration)\
                            from  choice as c, patient as p, doctor as d\
                            where  c.patient_ssn = p.SSN and p.age<65 and d.doctor_id = c.doctor_id\
                            group by c.doctor_id\
                            order by avg(c.duration)")
                data = c.fetchall()
                style = "{:<10}	{:<15}	{:<5}"
                print(style.format("ID","ΓΙΑΤΡΟΣ","ΜΕΣΟΣ ΟΡΟΣ"))
                for t in data:
                    print(style.format(t[0],t[1],t[2]))

            elif query == "4":
                #Query 4:Ποια ειδικοτητα γιατρου επισκεφτηκαν περισσοτερο οι γυναικες το 2019
                print("\nΕρώτηση 4: Ποιες 5 ειδικότητες επισκέφτηκαν περισσότερο οι γυναίκες το 2019;")
                c.execute("select d.speciality, count(*)\
                            from choice as c, patient as p, doctor as d\
                            where p.sex = 'FEMALE' and p.SSN = c.patient_ssn and c.year = 2019 and c.doctor_id = d.doctor_id\
                            group by d.speciality\
                            order by count(*) DESC limit 5")
                data = c.fetchall()
                style = ("{:<15}  {:<5}")
                print(style.format("ΕΙΔΙΚΟΤΗΤΑ","ΑΡΙΘΜΟΣ ΕΠΙΣΚΕΨΕΩΝ"))
                for t in data:
                    print(style.format(t[0],t[1]))

            elif query == "5":
                #Query 5:Ποιος ασθενής ακύρωσε τα περισσότερα ραντεβού που είχε προγραμματίσει για το 2023
                print("\nΕρώτημα 5: Ποιος ασθενής ακύρωσε τα περισσότερα ραντεβού που είχε προγραμματίσει για το 2023;")
                c.execute("select all p.SSN,p.lastname, count(*)\
                            from  patient as p, choice as c\
                            where c.app_state = 'CANCELLED'  AND\
                                c.year = 2023  and   c.patient_ssn = p.SSN \
                            group by p.lastname\
                            order by count(*) DESC limit 2")
                data = c.fetchall()
                style = ("{:<15}  {:<15}  {:<5}")
                print(style.format("SSN","ΕΠΩΝΥΜΟ", "ΑΡΙΘΜΟΣ ΑΚΥΡΩΜΕΝΩΝ ΡΑΝΤΕΒΟΥ"))
                for t in data:
                    print(style.format(t[0],t[1],t[2]))

            elif query == "6":
                #Query 6: Τι ωρα ξεκίνησαν τα περισσότερα ραντεβού του γιατρου

                print("\nΕρώτημα 6: Τι ώρα ξεκινάνε τα περισσότερα ραντεβού ενός γιατρού;")
                doc_id = input("Εισάγετε ID γιατρού:")
                script = ("select d.lastname, c.start_time, count(*)\
                            from choice as c, doctor as d\
                            where d.doctor_id = c.doctor_id and d.doctor_id ='", doc_id,"'\
                            group by c.start_time\
                            order by  count(*) DESC limit 1")
                script = ''.join(script)
                c.execute(script)
                data = c.fetchall()
                style = ("{:<15}  {:<10}  {:<5}")
                print(style.format("ΓΙΑΤΡΟΣ","ΩΡΑ", "ΑΡΙΘΜΟΣ ΡΑΝΤΕΒΟΥ"))
                for t in data:
                      print(style.format(t[0],t[1],t[2]))

            elif query == "7":
                #Query 7: Ποιους γιατρούς επισκέφτηκε ο  ταδε μεχρι το 2023
                print("\nΕρώτημα 7: Ποιους γιατρούς έχει επισκεφτεί ένας ασθενής;")
                number = input("Εισάγετε SSN ασθενούς:")
                script = ("select p.SSN, d.doctor_id, d.lastname, d.speciality\
                            from doctor as d, patient as p, choice as c\
                            where  p.SSN = c.patient_ssn and c.doctor_id =  d.doctor_id and c.year<2023 and p.SSN = '", number,"'")
                script = ''.join(script)
                c.execute(script)
                data = c.fetchall()
                style = ("{:<10}  {:<10}  {:<10}  {:<15}")
                print(style.format("SNN","ID", "ΓΙΑΤΡΟΣ", "ΕΙΔΙΚΟΤΗΤΑ"))
                for t in data:
                      print(style.format(t[0],t[1],t[2],t[3]))

            elif query == "8":
                #Query 8: Ποιοι γιατροί δεν ήταν στο νοσοκομείο 30/8/2020
                print("\nΕρώτημα 8: Ποιοι γιατροί δεν δούλευαν στις 30/8/2020;")
                c.execute("select d.lastname, d.firstname\
                            from doctor as d, Non_working as n\
                            where n.year = 2020 and n.month = 8 and n.day_num = 28 and d.doctor_id = n.doctor_id")
                data = c.fetchall()
                style = ("{:<15}  {:<15}")
                print(style.format("ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ"))
                for t in data:
                    print(style.format(t[0],t[1]))

            elif query == "9":
                #Query 9: Δείτε όλους τους γιατρούς μιας ειδικότητας
                print("\nΕρώτημα 9: Δείτε όλους τους γιατρούς μιας ειδικότητας.")
                spec = input("Εισάγετε το είδους του γιατρού:")
                spec = spec.upper()
                print(spec)
                script = ("select doctor_id, lastname, firstname from doctor where speciality = '", spec,"'")
                script = ''.join(script)
                c.execute(script)
                data = c.fetchall()
                style = ("{:<15}  {:<15}  {:<15}")
                print(style.format("ID","ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ"))
                for t in data:
                    print(style.format(t[0],t[1],t[2]))
            elif query == "10":
                #Query 10: Δείτε τους ασθενείς που έχουν επισκεφτει έναν γιατρό
                print("\nΕρώτημα 10: Δείτε τους ασθενείς που έχουν επισκεφτεί κάποιον γιατρό.")
                doc = input("Εισάγετε το ID του γιατρού:")
                script = ("select distinct p.ssn, p.lastname, p.firstname from patient as p,\
                            choice as c where c.patient_ssn = p.ssn and c.doctor_id ='",doc,"'")
                script = ''.join(script)
                c.execute(script)
                data = c.fetchall()
                style = ("{:<15}  {:<15}  {:<15}")
                print(style.format("SSN","ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ"))
                for t in data:
                    print(style.format(t[0],t[1],t[2]))
            elif query == "11":
                #Query 11: Δειτε τα προγραμματισμενα ραντεβου ενος γιατρου
                print("\nΕρώτημα 11:Δείτε τα προγραμματισμένα ραντεβού ενός γιατρού.")
                doc = input("Εισάγετε το ID του γιατρού:")
                script = ("select distinct c.patient_ssn, a.day_num, a.day_name, a.month, a.year, c.start_time\
                           from choice as c, appointment as a\
                           where c.year > 2022 and a.year = c.year and a.month = c.month\
                           and a.day_num = c.day_num and c.app_state = 'ACTIVE' and c.doctor_id = a.doctor_id and\
                           c.doctor_id = '", doc,"' order by a.year,a.month,a.day_num")
                script = ''.join(script)
                c.execute(script)
                data = c.fetchall()
                style = ("{:<15}  {:<5}  {:<10}  {:<5}  {:<5}  {:<5}")
                print(style.format("SSN","ΜΕΡΑ", "ΜΕΡΑ", "ΜΗΝΑΣ", "ΕΤΟΣ", "ΩΡΑ"))
                for t in data:
                    print(style.format(t[0],t[1],t[2],t[3],t[4],t[5]))
            elif query == "12":
                #Query 12: Δείτε τα ακυρωμενα ραντεβου ενος γιατρου
                print("\nΕρώτημα 12:Δείτε τα ακυρωμένα ραντεβού ενός γιατρού.")
                doc = input("Εισάγετε το ID του γιατρού:")
                script = ("select distinct c.patient_ssn, a.day_num, a.day_name, a.month, a.year, c.start_time\
                           from choice as c, appointment as a\
                           where c.year > 2022 and a.year = c.year and a.month = c.month\
                           and a.day_num = c.day_num and c.app_state = 'CANCELLED' and c.doctor_id = a.doctor_id and\
                           c.doctor_id = '", doc,"' order by a.year,a.month,a.day_num")
                script = ''.join(script)
                c.execute(script)
                data = c.fetchall()
                style = ("{:<15}  {:<5}  {:<10}  {:<5}  {:<5}  {:<5}")
                print(style.format("SSN","ΜΕΡΑ", "ΜΕΡΑ", "ΜΗΝΑΣ", "ΕΤΟΣ", "ΩΡΑ"))
                for t in data:
                    print(style.format(t[0],t[1],t[2],t[3],t[4],t[5]))
            elif query == "13":
                #Query 13: Δείτε τις μέρες που δεν δουλεύει στην κλινική ένας γιατρός για κάποιο έτος
                print("\nΕρώτημα 13: Δείτε τις μέρες που δεν δουλεύει στην κλινική ένας γιατρός για κάποιο έτος.")
                doc = input("Εισάγετε το του ID γιατρού:")
                etos = input("Εισάγετε το έτος:")
                script = ("select day_num, month, kind\
                            from Non_working\
                            where year = ",etos," and doctor_id = '",doc,"'\
                            order by month, day_num")
                script = ''.join(script)
                c.execute(script)
                data = c.fetchall()
                style = ("{:<5}  {:<5}  {:<10}  ")
                print(style.format( "ΜΕΡΑ", "ΜΗΝΑΣ", "AITIA"))
                for t in data:
                    print(style.format(t[0],t[1],t[2]))
                
            else: print("Σφάλμα: το ερώτημα ", query, " δεν βρέθηκε. Ξαναπροσπάθησε!")
                
                    

            


####################KΛΕΙΣΙΜΟ ΡΑΝΤΕΒΟΥ################################################################################################

    if action == "N" or action == "n":
        print("Είστε καταχωρημένος ασθενής;")       #πρώτα ελέγχουμε αν υπάρχει ο ασθενής στο σύστημα
        query = input("Πατήστε N για ναι και O για όχι:")
        if query == "O" or query == "o" :                            #αν όχι, πρώτα πρέπει να τον βάλουμε
            SSN = input("Πληκτρολογήστε το SSN σας:")
            script = ("select lastname from patient where SSN = '",SSN, "'")
            script = ''.join(script)
            c.execute(script)
            data = c.fetchall()
            if len(data)== 0 :
                firstname = input("Πληκτρολογήστε το μικρό όνομά σας:")
                lastname = input("Πληκτρολογήστε το επώνυμό σας:")
                sex = input("Πληκτρολογήστε FEMALE ή MALE:")
                age = input("ΠΛηκτρολογήστε την ηλικία σας:")
                phonenum = input("Πληκτρολογήστε το κινητό σας:")
                mail = input("Πληκτρολογήστε το email σας:")
                street = input("Πληκτρολογήστε τον δρόμο της οδός σας:")
                num = input("Πληκτρολογήστε τον αριθμό της οδούς σας:")
                c.execute("insert into patient values (?,?,?,?,?,?,?,?,?)",\
                           (SSN,firstname,lastname,sex,age,phonenum,mail,street,num))
                conn.commit()
                print("Επιτυχής καταχώρηση ασθενούς!")
            else: print("Υπάρχει ήδη καταχωρημένος ασθενής με SSN:",SSN)
            
        elif query == "N" or query == "n":
            doctor = input("Εισάγετε ID του γιατρού που επιθυμείτε να δείτε:")  #αν ναι, προχωραμε κατευθειαν στο κλείσιμο το ραντεβου
            script = ("select lastname from doctor where doctor_id = '",doctor,"'")
            script = ''.join(script)
            c.execute(script)
            check = c.fetchall()
            if len(check) == 0 : print("\nΔεν υπάρχει γιατρός με ID", doctor,"!")
            else:
                date = input("Εισάγετε ημερομηνία ραντεβού με μορφή d/m/yyyy :")
                time = input("Εισάγετε ώρα προτίμησης με μορφή tt:00 :")
                date = date.split("/",3)
                c.execute("select app_state from choice\
                                      where year = ? and month = ?\
                                      and day_num = ? and start_time = ? and doctor_id = ?",\
                                    (date[2],date[1],date[0], time, doctor))
                check1 = c.fetchall()
                c.execute("select year from non_working\
                                      where year = ? and month = ?\
                                      and day_num = ?  and doctor_id = ?",\
                                    (date[2],date[1],date[0], doctor))
                check2 = c.fetchall()
                if len(check2) != 0 : print("Ο γιατρός δεν δέχεται ραντεβού τότε.")
                else:
                    if len(check1) == 0:
                        print("Υπάρχει διαθεσιμότητα!")                 #ελεγχουμε για διαθεσιμοτητα
                        patient = input("Εισάγετε το SSN σας:")
                        script = ("select lastname from patient where ssn = '" ,patient,"'")
                        script = ''.join(script)
                        c.execute(script)
                        data2 = c.fetchall()
                        if len(data2) == 0 :
                            print("Δεν έχει καταχωρηθεί ασθενής με SSN:", patient)

                        else:
                            c.execute("select DayName from calendar where Year = ? and Month = ? and DayOfMonth = ?", \
                                                (date[2],date[1],date[0]))
                            day_name1 = c.fetchall()
                            day_name = day_name1[0]
                            day_name = ''.join(day_name)
                            day_name = day_name.upper()
                            if day_name == "SUNDAY":
                                print("Δεν μπορείτε να κλείσετε ραντεβού τις Κυριακές!")
                            else:
                                
                                c.execute("insert into choice values(?,?,?,?,?,?,?,?,?)",\
                                          (date[2],date[1],day_name,date[0],doctor,patient,"ACTIVE",time,""))
                                conn.commit()
                                date = "/".join(date)
                                script = ("select lastname, firstname, doctor_id from doctor where doctor_id = '",doctor,"'")
                                script = ''.join(script)
                                c.execute(script)
                                name = c.fetchall()
                                print("Επιτυχής καταχώρηση ραντεβού. Έχετε κλείσει ραντεβού με τον/την γιατρό"\
                                                ,name[0][0],name[0][1],name[0][2],"στις",date,"και ώρα", time,"." )
                    else : print("Δεν υπάρχει διαθεσιμότητα, δοκιμάστε άλλο ραντεβού.")
        else:
            print("Πίσω στην αρχική...")

    elif action == "0":
                print("Έξοδος...")
                break

    else: print("Δοκιμάστε ξανά!")


os.system("PAUSE")
conn.close()