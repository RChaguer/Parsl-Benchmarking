#! /bin/bash

py=python3.8
s_1=fibo.py
s_2=array_f.py
p=$(nproc --all)
file_1=benchmark_fibo_$p
file_2=benchmark_sq_$p

lscpu > full_setup_$p

for n in 5 8 10 12 15 20 
do
    $py $s_1 py $n None $file_1
    for c in htex thread
    do
        $py $s_1 parsl $n $c $file_1
    done
    echo "Testing Done for n :" $n 
done


for n in 5 10 25
do
    for t_h in 64 256 512 1024
    do
        for dur in None 0.0001 0.001
        do
            for t in py t mp
            do
                $py $s_2 $t $n None $t_h $dur $file_2
            done
            for c in htex thread
            do
                $py $s_2 parsl $n $c $t_h $dur $file_2
            done
        done
    done
    echo "Testing Done for n :" $n 
done