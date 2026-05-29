# README77331_V2m
*Extracted from: README77331_V2m.pdf*
*Date extracted: 2026-05-29 12:10:51*

---

## Page 1

Government of India.
Data Processing Division.
National Sample Survey Office.
164, Gopal Lal Thakur Road, Kolkata-108.
Phone No. 2577-1128.
---------------------------------------
NSS 77th Round.
Final Multiplier-posted unit-level data
for Schedule 33.1 of NSS 77th round Visit-II
A) Data for Sch. 33.1 (Land and Livestock Holding of Households and Situation Assessment
of Agricultural Households).
There are 17 data files belonging to 17 different levels as per layout
(NSS_77th_Layout_Sch_33.1_mult_post.xls).
File names No. of Records
r77s331v2L01.txt 56899
r77s331v2L02.txt 270952
r77s331v2L04.txt 165843
r77s331v2L05.txt 38671
r77s331v2L06.txt 88791
r77s331v2L07.txt 88791
r77s331v2L08.txt 262843
r77s331v2L10.txt 70988
r77s331v2L11.txt 70988
r77s331v2L12.txt 109277
r77s331v2L13.txt 7210
r77s331v2L14.txt 45137
r77s331v2L16.txt 35131
r77s331v2L17.txt 715762
r77s331v2L18.txt 55367
r77s331v2L19.txt 164066
r77s331v2L20.txt 45375
Total 2292091

---

## Page 2

Record length for data is 140 (including new-line character).
All the level wise data files are in text format.
B) Note for users :
1. These level wise data files are text data with fixed record-length of 140 characters
(including new-line character). First 126 bytes are data, following by 3 bytes comprise of
number of first stage units surveyed within a substratum for the sub-sample combined
(NSC) and next 10 bytes are weight or multiplier within a substratum (MLT). Last byte is
for Newline character.
2. The Layout of data is given in the MS Excel-file
NSS_77th_Layout_Sch_33.1_mult_post.xls.
3. In case of those Blocks/Levels, where Item/Person/Sl. No. etc is not applicable, the field is
filled up with "00000".
4. Crop code for “others” are recorded as ‘5999’ and “all” is recorded as ‘9999’
5. In the value fields (in Rs. or quantity or area etc.) the numeric figure is given in data file
along with decimal point whenever applicable.
6. For generating any estimate, one has to extract relevant portion of the data, and aggregate
after applying the weights.
7. Weights (or multipliers) are given at the end of each record from 130th byte onwards.
NSS and sub-stratum-wise weights:
NSS = Bytes 127-129 (3 bytes)
MLT = Bytes 130-139 (10 bytes, assumed two places of decimal)
All records of a second stage stratum will have same weight figure.
Final Weight = MLT/100
8. Common Primary Key for identification of a record for any schedule is:
FSU Serial Number = 4(5) (i.e., offset = 4th byte, length = 5 bytes)
Second Stage Stratum Number = 30(1)
household Number = 31(2)
Visit Number = 33(1)
Level Number = 34(2)
Item Code = 36(5)
9. For generating combined estimates based on the common set of households of visit 1 and
visit 2, visit 2 multipliers are to be used.
************

---

