
function readLanguageData(repo_url) {
    const repoURLComponents = repo_url.split("/");
    const repoName = repoURLComponents[repoURLComponents.length - 1];
    const url = `https://api.github.com/repos/cepdnaclk/${repoName}/languages`;

    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function(data) {
            var total = 0;
            var count = 0;
            var langList = {};
            $.each(data, function(lang, usage) {
                total += usage;
                count += 1;
                langList[lang] = usage;
            });

            if (count > 0) {
                $(".langData").removeClass("d-none");

                $.each(langList, function(lang, usage) {
                    var p = usage / total;
                    var val = Math.round(p * 10000) / 100;

                    if (val >= 0.25) {
                        $("#langList").append(`<li>${lang} - ${val}%</li>`);
                    }
                });
            }
        }
    });
}

function readAPIData(url) {

    const apiBase = 'https://api.ce.pdn.ac.lk/projects/v1';
    const projData = url.split('/');

    const projBatch = projData[2].toUpperCase();
    const projCat = projData[1];

    const projTitle = url.replace(`${projData[1]}/${projData[2]}/`, '');
    const apiURL = `${apiBase}/${projCat}/${projBatch}/${projTitle}`;

    // console.log(`${projData[1]}-${projData[2]}-`);
    // console.log(projData);

    console.log('Fetch data from the API,', apiURL);
    $.ajax({
        type: "GET",
        url: apiURL,
        dataType: "json",
        success: function(data) {

            // Show remoteData container
            $(".remoteData").removeClass("d-none");

            // console.log(data.team);

            // Team Data
            if (data.team && data.team[0] != "E/yy/xxx") {
                let teamCount = 0;

                $.each(data.team, function(index, member) {
                    if (index != "E/yy/xxx") {
                        let memberData = teamCard(member.name, member.profile_url, member.profile_image);

                        // console.log(memberData);
                        $("#teamCards").append(memberData);
                        teamCount++;
                    }
                });

                if(teamCount>0){
                    $(".remoteDataTeam_cards").removeClass("d-none");
                }
            }
        }
    });

}

function readRemoteData(page_url) {
    const url = `${page_url}/data/index.json`;

    console.log('Fetch data from the project config,', url);
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function(data) {

            // Show remoteData container
            $(".remoteData").removeClass("d-none");

            // Supervisor Data
            // if (data.supervisors[0].email != "email@eng.pdn.ac.lk") {
            //     let supervisorCount = 0;
            //
            //     $.each(data.supervisors, function(index, supervisor) {
            //         if (supervisor.email != "email@eng.pdn.ac.lk") {
            //             let supervisorData = '';
            //             supervisorData +=(`<li class="mb-4"><span>${supervisor.name}</span><br>`);
            //
            //             if(supervisor.email != "mail@eng.pdn.ac.lk" && supervisor.email != undefined){
            //                 supervisorData +=(`<span class="mx-2"><a class="text-dark" href="mailto:${supervisor.email}">
            //                 <i class='fa fa-envelope mx-2' aria-hidden='true'></i>${supervisor.email}
            //                 </a></span>`);
            //             }
            //
            //             if(supervisor.linkedin_profile != "#" && supervisor.linkedin_profile != undefined){
            //                 supervisorData +=(`<span class="mx-2"><i class='fa fa-linkedin mx-2' aria-hidden='true'></i>
            //                 <a class="text-dark" target="_blank" href="${supervisor.linkedin_profile}">Linkedin</a></span>`);
            //             }
            //             if(supervisor.website != "#" && supervisor.website != undefined){
            //                 supervisorData +=(`<span class="mx-2"><i class='fa fa-globe mx-2' aria-hidden='true'></i>
            //                 <a class="text-dark" target="_blank" href="${supervisor.website}">Website</a></span>`);
            //             }
            //             if(supervisor.researchgate_profile != "#" && supervisor.researchgate_profile != undefined){
            //                 supervisorData +=(`<span class="mx-2"><i class='fab fa-researchgate"></i mx-2' aria-hidden='true'></i>
            //                 <a class="text-dark" target="_blank" href="${supervisor.researchgate_profile}">Researchgate</a></span>`);
            //             }
            //
            //             supervisorData+= '</li>';
            //             $("#supervisorList").append(supervisorData);
            //             supervisorCount++;
            //         }
            //     });
            //
            //     if(supervisorCount >0){
            //         $(".remoteDataSupervisors").removeClass("d-none");
            //     }
            // }

            // Tag Data
            if (data.tags.length > 0) {
                $(".remoteDataTags").removeClass("d-none");
                $.each(data.tags, function(index, tag) {
                    $("#tagList").append(`<span class='tag m-2'>${tag}</span> `);
                });
            }

            // Publication details
            if (data.publications != null && data.publications.length > 0) {
                let count = 0;

                $.each(data.publications, function(index, pub) {
                    // "title":"Paper Title",
                    // "journal":"Journal or Conference Name",
                    // "description":"Sample Description",
                    // "url":"#"

                    if (
                        pub.title !== "Paper Title" &&
                        pub.journal !== "Journal or Conference Name" &&
                        pub.description !== "Sample Description"
                    ) {
                        $("#publicationsURL").append("<li><div>");
                        $("#publicationsURL").append(
                            "<a href='" + pub.url + "' target='_blank'>" + pub.title + "</a>, " + pub.journal + "<br>"
                        );
                        $("#publicationsURL").append(
                            "<small>" + pub.description + "</small>"
                        );
                        $("#publicationsURL").append("</div></li>");
                    }
                });

                if (count > 0) {
                    $("#publications").removeClass("d-none");
                }
            }

            if (data.media != null && data.media.length > 0) {
                let count = 0;

                $.each(data.media, function(index, media) {
                    if (media.type === "youtube" && media.url.length > 0) {
                        if (!(media.title == "" || media.url =="#")) {
                            // Show the title

                            if(media.title != undefined ){
                                $("#youtubeVideoDiv").append("<h4>" + media.title + "</h4>");
                            }

                            $("#youtubeVideoDiv").append(
                                "<div class='video-container'><iframe width='100%' src='" +
                                media.url +
                                "' frameborder='1' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen=''>"
                            );
                            $("#youtubeVideoDiv").append("</iframe></div>");
                            $("#youtubeVideoDiv").append("<br><br>");
                            count++;
                        }
                    } else {
                        // Only supported youtube videos for now
                    }
                });

                if (count > 0) {
                    $("#youtubeVideo").removeClass("d-none");
                }
            }

            // Removed, since it is already provided
            // $("#descriptionText").html(`<p>${data.description}</p>`);
        }
    });
}


function teamCard(name, profile_url, avatar_url){
    return `<div class="col-4 col-sm-3 col-md-2 col-lg-2 d-flex" style="padding: 3px;">
    <div class="card p-1 flex-fill">
    <div class="overflow-hidden">
    <img class="card-img-top img-fluid" src="${avatar_url}" alt="Card image">
    </div>
    <div class="card-body p-0 d-flex flex-column">
    <h4 class="profile-title card-title text-center pt-1">${name}</h4>
    <p class="profile-text card-text text-center">E/15/140</p>
    <div class="d-grid mt-auto px-2 pb-2">
    <a href="${profile_url}" target="_blank" class="btn btn-sm btn-primary btn-block">See Profile</a>
    </div>
    </div>
    </div>
    </div>`
}
