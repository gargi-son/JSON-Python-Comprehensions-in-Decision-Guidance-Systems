import json

def imply(lhs,rhs):
    return((not lhs) or rhs)

# student sat'd course prereq's with B or better

def studentGotAorB(ssn, dcode, cno, transcript):
    # replace with correct implementation
    aOrB = True
    return(aOrB)

def studentSatCoursePrereqs(ssn,dcode,cno,univDB):
    #replace with correct implementation
    prereqsSatisfied = True
    return(prereqsSatisfied)

def studentSatClassPrereqs(ssn,cl,univDB):
    # replace with correct implementations
    prereqsSatisfied = True
    return(prereqsSatisfied)

def queries(univDB):
    tables = univDB["tables"]
    department = tables["department"]
    course = tables["course"]
    prereq = tables["prereq"]
    class_ = tables["class"]
    faculty = tables["faculty"]
    student = tables["student"]
    enrollment = tables["enrollment"]
    transcript = tables["transcript"]

#    find all CS students
    q1 = [
        { "ssn": s["ssn"], "name": s["name"]}
        for s in student
        if s["major"] == "CS"
    ]
    q1.sort(key = lambda s: s["ssn"])

# find CS students who are enrolled in a MTH class

    q2 = [
        { "ssn": s["ssn"], "name": s["name"]}
        for s in student
        if s["major"] == "CS"
        if any([
             ( e["ssn"] == s["ssn"] and
                e["class"] == c["class"] and
                c["dcode"] == "MTH")
             for e in enrollment
             for c in class_
        ])
        ]
    q2.sort(key = lambda s: s["ssn"])

    q2a = [
        { "ssn": s["ssn"], "name": s["name"]}
        for s in student
        if s["major"] == "CS"
        if any([
             true
             for e in enrollment
             for c in class_
             if ( e["ssn"] == s["ssn"] and
                e["class"] == c["class"] and
                c["dcode"] == "MTH")
        ])
        ]
    q2a.sort(key = lambda s: s["ssn"])

    q2_ssn_set = {
        s["ssn"]
        for s in student
        if s["major"] == "CS"
        for e in enrollment
        if s["ssn"] == e["ssn"]
        for c in class_
        if c["class"] == e["class"] and c["dcode"] == "MTH"
    }

    q2_ssn_set_another_version = {
        s["ssn"]
        for s in student
        for e in enrollment
        for c in class_
        if s["major"] == "CS"
        if s["ssn"] == e["ssn"]
        if c["class"] == e["class"] and c["dcode"] == "MTH"
    }

    q2b = [
        s
        for s in student
        for ssn in q2_ssn_set
        if s["ssn"] == ssn
    ]
    q2b.sort(key = lambda t: t["ssn"])

#  The student with ssn = 10 is enrolled in a math class

    q3 = any([ (e["ssn"] == 10 and
                c["class"] == e["class"] and
                c["dcone"] == "MTH")
        for e in enrollment
        for c in class_
    ])
# the student w/ssn = 10 is enrolled in ALL math classes

    def enrolledIn(c):
        return any([e["ssn"]==10 and e["class"]==c["class"]
                for e in enrollment
        ])
    mathClasses = [ c for c in class_ if c["dcode"]=="MTH"]

    q3_with_ALL = all([enrolledIn(c) for c in mathClasses])

    q3_another_variant = any([ True
        for e in enrollment
        for c in class_
        if e["ssn"] == 10 and
           c["class"] == e["class"] and
           c["dcone"] == "MTH"
    ])

# all CS students who are enrolled in a math class
    q2_yet_another_variant = [ s
        for s in student
        if s["major"] == "CS"
        if # s is enrolled in a MTH class
            any([ (e["ssn"] == s["ssn"] and
                        c["class"] == e["class"] and
                        c["dcode"] == "MTH")
            for e in enrollment
            for c in class_
            ])
        ]
    q2_yet_another_variant.sort(key = lambda t: t["ssn"])

# all CS students who are enrolled in ALL math classes

    q3 = [ s
        for s in student
        if s["major"] == "CS"
        if # s is enrolled in ALL math classes
            all([
                # s is enrolled in c
                any([
                    e["ssn"] == s["ssn"] and e["ssn"] == c["class"]
                    for e in enrollment
                ])
                for c in class_
                if c["dcode"] == "MTH"
            ])
    ]
    q3.sort(key = lambda t: t["ssn"])
    def enrolledIn(ssn, c):
        return any([ ssn == e["ssn"] and e["class"]==c["class"]
                for e in enrollment
        ])

    q3a = [ s
        for s in student
        if s["major"]=="CS"
        if all([ enrolledIn(s["ssn"],c)
            for c in class_
            if c["dcode"]=="MTH"
        ])
    ]
    q3a.sort(key=lambda t: t["ssn"])

# all students named John Smith has taken the course CS 530
#    q4 = "tbd"
# Boolean: Professor Brodsky teaches all classes in which "Tom Smith" is enrolled
    def brodskyTeaches(c):
        return any([ f["ssn"]==c["instr"] and f["name"]=="Brodsky"
                for f in faculty
        ])
    classesWTom = { c
                    for c in class_
                    for e in enrollment
                    for s in student
                    if c["class"]==e["class"]
                    if e["ssn"]==s["ssn"]
                    if s["name"]=="Tom Smith"
    }
    q4 = all([ brodskyTeaches(c)
            for c in classesWTom
    ])
# A is a subset of B
# A is the set of classes where Tom Smith is enrolled
# B is the set of classes taught by Brodsky

    A = [ c
	for e in enrollment
	for c in class_
	if(c["class"] == e["class"])
	for s in student
	if s["ssn"]==e["ssn"] and s["name"] == "Tom Smith"
	]

# (all x in A) BB(x)
    q5 =  all([
                any([
                    (c["instr"] == f["ssn"] and f["name"] == "Brodsky")
                    for f in faculty
                ])
                for c in A
    ])

# (all x in U) (A(x) --> B(x))

    def JohnIsEnrolled(c):
        result = any([
            ( e["ssn"] == s["ssn"] and s["name"]  == "John Smith" and e["class"] == c["class"])
            for e in enrollment
            for s in student
        ])
        return result

    def taughtByBrodsky(c):
        result = any([
            ( c["instr"] == f["ssn"] and f["name"] == "Brodsky")
            for f in faculty
        ])
        return result


    q5a = all([
        imply( JohnIsEnrolled(c), taughtByBrodsky(c) )
        for c in class_
    ])


# Data: find those professors who teach all classes in which a student named "Tom Smith" is enrolled

    tom_classes = { c
        for c in class_
        if any([ (s["ssn"] == e["ssn"] and s["name"] == "Tom Smith" and c["class"] == e["class"])
                for s in student
                for e in enrollment
            ])
    }
    q6 = [
        f
        for f in faculty
        if # f teaches all classes in which Tom is enrolled
           # (all c in Tom classes) (f is teaching c)
            all([
                # f teaches c
                c["instr"] == f["ssn"]
                for c in tom_classes
            ])
    ]
    q6.sort(key=lambda t: t["ssn"])
# start dataQuery C from HA2
    q7 = [ s
        for s in student
        if   # s sat'd all prereqs of all classes she is enrolled in
            all([
                studentSatClassPrereqs(s["ssn"], e["class"], univDB)
                for e in enrollment
                if e["ssn"] == s["ssn"]
            ])

    ]
    q7.sort(key = lambda t: t["ssn"])
#alt solution
    q8 = [ s
        for s in student
        if   # s sat'd all prereqs of all classes she is enrolled in
            all([ imply(s["ssn"] == e["ssn"],
                    studentSatClassPrereqs(e["ssn"], e["class"], univDB)
                  )
                for e in enrollment
            ])

    ]
    q8.sort(key = lambda t: t["ssn"])
# there is a student w/ ssn = 82

    q8a = any([ s["ssn"] == 82
                for s in student
            ])

    q8b = any([ True
                for s in student
                if s["ssn"] == 82
            ])
#boolQuery D
    #replace w/correct implementation

    def satisfy_prereq(ssn,dcode,code):
        return True
    #replace w/correct implementation
    def student_enrollments(ssn):
        return enrollment


    q9 = any([ # student s sat'd all prereqs of all classes she's enrolled in
            all([satisfy_prereq(s["ssn"], c["dcode"], c["cno"])
                     for e in student_enrollments(s["ssn"])
                     for c in class_
                     if e["class"]==c["class"]
            ])
            for s in student
            if s["ssn"] == 82
    ])

# Data: find professors who teach a class with 3 or more prerequisites
    def has3orMorePrereqs(c):
        return (len([p
                    for p in prereq
                    if p["dcode"] == c["dcode"]
                    and p["cno"] == c["cno"]
                ]) >= 3
        )

    q10 = [
        f
        for f in faculty
        if # teaches a class w/3 or more prereqs
            any([
                c["instr"] == f["ssn"] and has3orMorePrereqs(c)
                for c in class_
            ])
    ]

#-----------------
    def getClassPrereqs(cl):
        classPrereqs = [
            pr
            for pr in prereq
            if pr["dcode"] == cl["dcode"] and
               pr["cno"]   == cl["cno"]
        ]
        return classPrereqs

    q10a = [
        fa
        for fa in faculty
        if any([
            len(getClassPrereqs(cl)) >= 3 and cl["instr"] == fa["ssn"]
            for cl in class_
        ])
    ]
    q11 = "tbd"
    q12 = "tbd"
    q13 = "tdb"
    q14 = "tbd"
    q15 = "tbd"
    q16 = "tbd"
    return({
        "q1": q1,
        "q2": q2,
        "q2a": q2a,
        "q2b": q2b,
        "q2_yet_another_variant":q2_yet_another_variant,
        "q3": q3,
        "q3a": q3a,
        "q4": q4,
        "q5": q5,
        "q5a": q5a,
        "q6": q6,
        "q7": q7,
        "q8": q8,
        "q8a": q8a,
        "q8b": q8b,
        "q9": q9,
        "q10": q10,
        "q10a": q10a,
        "q11": q11,
        "q12": q12,
        "q13": q13,
        "q14": q14,
        "q15": q15,
        "q16": q16
    })
f = open("../../testDBs/db1.json", "r")
db1 = json.loads(f.read())
f = open("../../testDBs/db2.json", "r")
db2 = json.loads(f.read())
f = open("../../testDBs/db3.json", "r")
db3 = json.loads(f.read())
f = open("../../testDBs/db4.json", "r")
db4 = json.loads(f.read())
f = open("../../testDBs/db5.json", "r")
db5 = json.loads(f.read())
f = open("../../testDBs/db6.json", "r")
db6 = json.loads(f.read())
f = open("../../testDBs/db7.json", "r")
db7 = json.loads(f.read())
f = open("../../testDBs/db8.json", "r")
db8 = json.loads(f.read())
f = open("../../testDBs/db9.json", "r")
db9 = json.loads(f.read())
f = open("../../testDBs/db10.json", "r")
db10 = json.loads(f.read())
f = open("../../testDBs/db11.json", "r")
db11 = json.loads(f.read())
f = open("../../testDBs/db12.json", "r")
db12 = json.loads(f.read())

answers = {
  "db1": queries(db1),
  "db2": queries(db2),
  "db3": queries(db3),
  "db4": queries(db4),
  "db5": queries(db5),
  "db6": queries(db6),
  "db7": queries(db7),
  "db8": queries(db8),
  "db9": queries(db9),
  "db10": queries(db10),
  "db11": queries(db11),
  "db12": queries(db12),
}
# print(json.dumps(answers))

with open('example_answers.json', 'w') as f:
    json.dump(answers, f)
