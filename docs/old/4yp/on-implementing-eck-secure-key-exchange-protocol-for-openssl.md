---
layout: project_old
title: On Implementing eCK-secure Key Exchange Protocol for OpenSSL
permalink: /4yp/e12/on-implementing-eck-secure-key-exchange-protocol-for-openssl

has_children: false
parent: E12 Final Year Projects
grand_parent: Final Year Projects

cover_url: https://cepdnaclk.github.io/projects.ce.pdn.ac.lk/data/categories/4yp/cover_page.jpg
thumbnail_url: /data/categories/4yp/thumbnail.jpg

tags: [	Computer and Network Security ]
team: [ Seralahthan Vivekaananthan, Nishen Peiris, Chamith Shanaka ]
supervisors: [ Dr. Janaka Alawatugoda ]

has_publication: true
publication: "Alawatugoda, J.; Seralathan, V.; Peiris, N.; Wickramasinghe, C. and Chuah, C.W. Implementation of an eCK-secure Key Exchange Protocol for OpenSSL. In International Journal on Advanced Science, Engineering and Information Technology, Volume 8, Issue 5, pages 2205-2210, INSIGHT – Indonesian Society for Knowledge and Human Development, 2018. Funding: H082"
---

Security models for two-party authenticated key exchange (AKE) protocols have developed over time to capture the security of AKE protocols even when the adversary learns certain secret values by some means (leakage due to weak random number generators, malware attacks, man-in-the-middle attacks, insider attacks etc). LaMacchia, Lauter and Mityagin presented a strong security model for AKE protocols, namely the extended Canetti–Krawczyk (eCK) model  (ProvSec 2007), addressing wide range of real-world attack scenarios. They constructed a protocol, known as the NAXOS protocol. In order to satisfy the definition of eCK security, the NAXOS protocol uses a hash function to combine the longterm and the ephemeral secret keys, which is widely known as NAXOS-trick. However, for protocols based on the NAXO-Strick, the way of leakage modelled in the eCK security model leads to an unnatural assumption of leak-free computation of the hash of the long-term secret key and the ephemeral secret key; because the eCK model allows the attacker to reveal ephemeral key while the NAXOS-trick computation output remains safe. In a recent work of Alawatugoda, Stebila and Boyd (IMA Cryptography and Coding 2015), a NAXOS- trick-free eCK-secure AKE protocol is presented, namely the protocol P1. In this work we implement the protocol P1 to be used with the widely-used cryptographic library, the OpenSSL library. OpenSSL implementations are widely used with the real-world security protocol suites, such as Security Socket Layer (SSL) and Transport Layer Security (TLS). As per best of our knowledge, this implementation is the first OpenSSL implementation of an eCK-secure key exchange protocol. Thus, we open up the direction to use the recent advancements of cryptography for real-world Internet communication.