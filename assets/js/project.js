function readLanguageData(repo_url) {
    const repoURLComponents = repo_url.split("/");
    const repoName = repoURLComponents[repoURLComponents.length - 2];
    const url = `https://api.github.com/repos/cepdnaclk/${repoName}/languages`;

    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function (data) {
            var total = 0;
            var count = 0;
            var langList = {};
            $.each(data, function (lang, usage) {
                total += usage;
                count += 1;
                langList[lang] = usage;
            });

            if (count > 0) {
                $(".langData").removeClass("d-none");

                $.each(langList, function (lang, usage) {
                    var p = usage / total;
                    var val = Math.round(p * 10000) / 100;

                    if (val >= 0.25) {
                        $("#langList").append(`<li>${lang} - ${val}%</li>`);
                    }
                });
            }
        },
    });
}

function readRemoteData(page_url) {
    const url = `${page_url}/data/index.json`;

    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function (data) {
            let visibility = true; // data.visibility

            if (visibility == true) {
                // Show remoteData container
                $(".remoteData").removeClass("d-none");

                if(data.team[0] != "Team Member Name 1" ){
                    $(".remoteDataTeam").removeClass("d-none");
                    $.each(data.team, function (index, member) {
                        $("#teamList").append(
                            `<li>${member.eNumber}, ${member.name}, <a href="mailto:${member.email}">${member.email}</a></li>`
                        );
                    });
                }

                if(data.supervisors[0] != "Dr. Supervisor 1" ){
                    $(".remoteDataSupervisors").removeClass("d-none");
                    $.each(data.supervisors, function (index, s) {
                        $("#supervisorList").append(
                            `<li>${s.name}, <a href="mailto:${s.email}">${s.email}</a></li>`
                        );
                    });
                }

                if(data.tags.length > 0){
                    $(".remoteDataTags").removeClass("d-none");
                    $.each(data.tags, function (index, tag) {
                        $("#tagList").append(`<span class='tag'>${tag}</span> `);
                    });
                }

                // Removed, since it is already provided
                // $("#descriptionText").html(`<p>${data.description}</p>`);
            }
        },
    });
}
