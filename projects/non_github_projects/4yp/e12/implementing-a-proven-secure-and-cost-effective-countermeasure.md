---
layout: project_old
title: Implementing a Proven-secure and Cost-effective Countermeasure against the Compression Ratio Info-leak Mass Exploitation (CRIME) Attack
permalink: /4yp/e12/implementing-a-proven-secure-and-cost-effective-countermeasure

has_children: false
parent: E12 Undergraduate Research Projects
grand_parent: Undergraduate Research Projects

cover_url: https://cepdnaclk.github.io/projects.ce.pdn.ac.lk/data/categories/4yp/cover_page.jpg
thumbnail_url: /data/categories/4yp/thumbnail.jpg

tags: ["Computer and Network Security"]
team: ["Jayamine Alupotha", "Sanduni Prasadi", "Mohamed Fawsan"]
supervisors: [Prof. Roshan G. Ragel, Dr. Janaka Alawatugoda]

has_publication: true
publication: "Alupotha, J.; Prasadi, S.; Fawzan, M.; Alawatugoda, J. and Ragel, R. Implementing a Proven-secure and Cost-effective Countermeasure against the Compression Ratio Info- leak Mass Exploitation (CRIME) Attack. In Proceedings of the 12th IEEE International Conference on Industrial and Information Systems (ICIIS 2017), IEEE Press, 2017. Funding: NRC 16-020"
---

Header compression is desirable for network applications as it saves bandwidth and reduces latency. However, when data is compressed before being encrypted, the amount of compression leaks information about the amount of redundancy in the plaintext. In web requests, headers contain secret web cookies. Therefore, compression of headers before encryption will reveal the information about the secret web cookies. This side-channel has led to Compression Ratio Info-leak Made Easy (CRIME) attack on web traffic protected by the SSL/TLS protocols. In order to mitigate the CRIME attack, compression is completely disabled at the TLS/SSL layer, which in return increases the bandwidth consumption and latency. In a previous work (Financial Cryptography and Data Security 2015), two countermeasures are presented with formal security proofs, against compression side-channel attacks, namely (1)–separating secret cookies from user inputs and (2)–using a static compression dictionary. In this work we create a test environment to replicate the CRIME attack and verify the attack. Moreover, we implement a proven-secure countermeasure against the CRIME attack, in a real world client/server setup, following the aforementioned two countermeasures. Our implementation achieves better compression ratio (closer to the original TLS/SSL compression), and hence reduces the bandwidth usage and latency significantly (therefore cost-effective). To the best of our knowledge, this is the first proven-secure and cost-effective countermeasure implementation against the CRIME attack.
