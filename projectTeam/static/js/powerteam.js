﻿var app = angular.module('PowerTeam', []);
var x=[];
counter=0;
var INTEGER_REGEXP = /^\-?\d*$/;
app.directive('integer', function () {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function (viewValue) {
                if (INTEGER_REGEXP.test(viewValue)) {
                    ctrl.$setValidity('integer', true);
                    return viewValue;
                } else {
                    ctrl.$setValidity('integer', false);
                    return undefined;
                }
            });
        }
    };
});


app.directive('myitem', function() {
	return {
		
	    restrict: 'E',
	    template: '',
	    transclude: true,


        link : function(scope, element, attrs) {

            scope.toggle = function toggle() {

            }
        }
	}
});

app.directive('onFinishRenderFilters', function ($timeout) {
    return {
        restrict: 'A',
        link: function(scope, element, attr) {
            if (scope.$last === true) {
                $timeout(function() {
                    scope.$emit('ngRepeatFinished');
                });
            }
        }
    };
});

$(function () {
    $('input, textarea').placeholder();
    $('.default-focus').focus();
    $("[data-toggle='tooltip']").tooltip();
    $(".tooltips").tooltip();
    $('*').tooltip({
        selector: "[data-toggle=tooltip]",
        container: "body"
    });
});

app.filter('to_trusted', ['$sce', function ($sce) {
    return function (text) {
   return $sce.trustAsHtml(text);
    };
}]);

function LoginCtrl($scope, $http) {
    $scope.isMatch = true;
    $scope.isDisabled = false;
    $scope.login = function () {
        $scope.isMatch = true;
        $scope.isDisabled = false;
        var btn = $("#btnLogin");
        btn.button('loading');
        $http.post('/Login', $scope.User).success(function (result) {
            btn.button('reset');
            if (result.isMatch != null) {
                $scope.isMatch = result.isMatch;
            }
            if (result.isDisabled != null) {
                $scope.isDisabled = result.isDisabled;
            }
            if (result.isMatch != null && result.isMatch) {
                window.location.href = '/Project';
            }
        });
    }
}

function RegisterCtrl($scope, $http) {
    $scope.userExist = false;
    $scope.register = function () {
        $scope.userExist = false;
        var btn = $("#btnRegister");
        btn.button('loading');
        $http.post('/Register/Save', $scope.User).success(function (result) {
            btn.button('reset');
            if (!result.created) {
                $scope.userExist = true;
            }
            else {
                window.location.href = '/Project';
            }
        });
    }
}

function ProjectCtrl($scope, $http) {
    $scope.ProjectList = [];
    $scope.ProjectList2 = [];
    $scope.p = [];
    $scope.Query = { PageNo: 1, ProjectName: '', ProjectKey: '', Introduction: '', Status: 1, RowCount: 0, PageCount: 0 };
    $scope.create = function () {
        var btn = $("#btnCreateProject");
        btn.button('loading');
        $http.post('/Project/Create', $scope.Project).success(function (result) {
            btn.button('reset');
            if (result.empty) {
            	$scope.isEmpty = true;
            	alert("项目名称或key值不能为空");
            }
            else {
	            if (result.exist) {
	                $scope.keyExist = true;
	//                alert($scope.keyExist)
	            }
	            else {
	            	//$scope.Project.ProjectName = '';
	            	//$scope.Project.ProjectKey = '';
	            	//$scope.Project.Introduction = '';
	                $('#project_add').modal('hide');
	                $scope.query();
	                //window.location.href = "/Project";
	            }
	        }
            //if (result.created) {
            //    $('#project_add').modal('hide');
            //    $scope.query();
            //}
        });
    }
    $scope.query = function () {
        var btn = $("#btnQuery");
        btn.button('loading');
        $http.post('/Project/Query', $scope.Query).success(function (result) {
            btn.button('reset');
            $scope.ProjectList = result.data;
            $scope.ProjectList2 = result.data2;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
            $scope.height = GetHeight()
        });
    }
}

function ProjectUpdateCtrl($scope, $http) {
    $scope.UpdateSuccess = false;
    $scope.DeleteSuccess = false;
    $scope.Delete = function () {
        var btn = $("#btnDelete");
        btn.button('loading');
        $http.post('/Project/Delete', { ProjectId: $scope.Project.ProjectId }).success(function (result) {
            if (result.deleted) {
                $scope.DeleteSuccess = true;
                btn.button('reset');
                window.location.href = '/Project';
            }
        });
    }
    $scope.update = function () {
        var btn = $("#btnUpdate");
        btn.button('loading');
        $http.post('/Project/Update', $scope.Project).success(function (result) {
            if (result.updated) {
                $scope.UpdateSuccess = true;
                btn.button('reset');
                window.location.href = '/Project';
            }
        });
    }
}

function TaskCtrl($scope, $http) {
    $scope.TaskList = [];
    $scope.Query = { PageNo: 1, TaskName: '',ProjectId:'all',AssignTo: -1, New: true, InProgress: true, Completed: false, Canceled: false, RowCount: 0, PageCount: 0 };
    $scope.query = function () {
        var btn = $("#btnQuery");
        btn.button('loading');
        $http.post('/Task/Query', $scope.Query).success(function (result) {
            btn.button('reset');
            $scope.TaskList = result.data;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }
}

function TaskCreateCtrl($scope, $http) {
    $scope.AddSuccess = false;
    editor = UE.getEditor('editor');
    $scope.Task = { TaskName: null, Versions: null,ProjectModuleId:'', Priority: 2, AssignTo: -1, Description: null };
    $scope.create = function () {
        var btn = $("#btnCreate");
        btn.button('loading');
        $scope.Task.Description = editor.getContent();
        $http.post('/Task/CreateNew', $scope.Task).success(function (result) {
        	if (result.created) {
                $scope.AddSuccess = true;
                btn.button('reset');
                window.location.href = "/Project/Task/" + result.ProjectId;
            }
        });
    }
}


function TaskUpdateCtrl($scope, $http) {
    $scope.UpdateSuccess = false;
    $scope.DeleteSuccess = false;
    $scope.ShowUpdate = false;
    $scope.edit = function () {
        $scope.ShowUpdate = !$scope.ShowUpdate;
        UE.getEditor('editor');
    }
    $scope.update = function () {
        var btn = $("#btnUpdate");
        btn.button('loading');
        $scope.Task.Feedback = UE.getEditor('editor').getContent();
//        $http.post('/Issue/Update', $scope.Issue).success(function (result) {
//            if (result.updated) {
//                $scope.UpdateSuccess = true;
//                btn.button('reset');
//                window.location.href = "/Project/Issue/" + $scope.Issue.ProjectId;
//            }
//        });
//    }
//    $scope.update = function () {
//        var btn = $("#btnUpdate");
//        btn.button('loading');
//        $scope.Task.Description = editor.getContent();
        $http.post('/Task/Update', $scope.Task).success(function (result) {
            if (result.updated) {
                $scope.UpdateSuccess = true;
                btn.button('reset');
                window.location.href = "/Project/Task/" + $scope.Task.ProjectId;
            }
        });
    }
    $scope.Delete = function () {
        var btn = $("#btnDelete");
        btn.button('loading');
        $http.post('/Task/Delete', { 'TaskId': $scope.Task.TaskId }).success(function (result) {
        	if (result.deleted) {
                $scope.DeleteSuccess = true;
                btn.button('reset');
                window.location.href = "/Project/Task/" + $scope.Task.ProjectId;
            }
        });
    }
}

function TeamCtrl($scope, $http) {
    $scope.AddSuccess = false;
    $scope.RemoveSuccess = false;
    $scope.MemberCandidate = [];
    $scope.MemberList = [];
    $scope.GetMemberCandidate = function () {
        $http.post('/Team/GetMemberCandidate', { 'ProjectId': $scope.ProjectId }).success(function (result) {
            $scope.MemberCandidate = result.data;
        });
    }
    $scope.GetMemberInProject = function () {
        $http.post('/Team/GetMemberInProject', { 'ProjectId': $scope.ProjectId }).success(function (result) {
            $scope.MemberList = result.data;
        });
    }
    $scope.AddMember = function (email) {
        $scope.AddSuccess = false;
        $scope.RemoveSuccess = false;
        $http.post('/Team/AddMember', { 'ProjectId': $scope.ProjectId, 'Email': email }).success(function (result) {
            if (result.created) {
                $scope.AddSuccess = true;
                $scope.GetMemberCandidate();
                $scope.GetMemberInProject();
            }
        });
    }
    $scope.RemoveMember = function (userId) {
        $scope.AddSuccess = false;
        $scope.RemoveSuccess = false;
        $http.post('/Team/RemoveMember', { 'ProjectId': $scope.ProjectId, 'UserId': userId }).success(function (result) {
            if (result.removed) {
                $scope.RemoveSuccess = true;
                $scope.GetMemberCandidate();
                $scope.GetMemberInProject();
            }
        });
    }
}

function IssueCtrl($scope, $http) {
    $scope.IssueList = [];
    $scope.Query = { PageNo: 1, Subject: '', AssignTo: -1, CategoryId: -1, Open: true, Fixed: false, Closed: false, Canceled: false, RowCount: 0, PageCount: 0 };
    $scope.query = function () {
        var btn = $("#btnQuery");
        btn.button('loading');
        $http.post('/Issue/Query', $scope.Query).success(function (result) {
            btn.button('reset');
            $scope.IssueList = result.data;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }
}

function IssueCreateCtrl($scope, $http) {
    $scope.AddSuccess = false;
    editor = UE.getEditor('editor');
    $scope.Issue = { Subject: null, ProjectModuleId:'',AssignTo: -1, Priority: 2, Description: null, CategoryId: -1 };
    $scope.create = function () {
        var btn = $("#btnCreate");
        btn.button('loading');
        $scope.Issue.Description = editor.getContent();
        $http.post('/Issue/CreateNew', $scope.Issue).success(function (result) {
            if (result.created) {
                $scope.AddSuccess = true;
                btn.button('reset');
                window.location.href = "/Project/Issue/" + result.ProjectId;
            }
        });
    }
}

function IssueUpdateCtrl($scope, $http) {
    $scope.UpdateSuccess = false;
    $scope.DeleteSuccess = false;
    $scope.ShowUpdate = false;
    $scope.edit = function () {
        $scope.ShowUpdate = !$scope.ShowUpdate;
        UE.getEditor('editor');
    }
    $scope.update = function () {
        var btn = $("#btnUpdate");
        btn.button('loading');
        $scope.Issue.Feedback = UE.getEditor('editor').getContent();
        $http.post('/Issue/Update', $scope.Issue).success(function (result) {
            if (result.updated) {
                $scope.UpdateSuccess = true;
                btn.button('reset');
                window.location.href = "/Project/Issue/" + $scope.Issue.ProjectId;
            }
        });
    }
    $scope.Delete = function () {
        var btn = $("#btnDelete");
        btn.button('loading');
        $http.post('/Issue/Delete', { 'IssueId': $scope.Issue.IssueId }).success(function (result) {
            if (result.deleted) {
                $scope.DeleteSuccess = true;
                btn.button('reset');
                window.location.href = "/Project/Issue/" + $scope.Issue.ProjectId;
            }
        });
    }
}

function UpdateProfileCtrl($scope, $http) {
    $scope.UpdateSuccess = false;
    $scope.Error = false;
    $scope.update = function () {
        $scope.UpdateSuccess = false;
        $scope.Error = false;
        var btn = $("#btnUpdateProfile");
        btn.button('loading');
        $http.post('/UpdateProfile', $scope.User).success(function (result) {
            if (result.Updated) {
                $scope.UpdateSuccess = true;
                $scope.Error = false;
            }
            else {
                $scope.UpdateSuccess = false;
                $scope.Error = true;
            }
            btn.button('reset');
        });
    }
}

function ChangePasswordCtrl($scope, $http) {
    $scope.UpdateSuccess = false;
    $scope.Error = false;
    $scope.update = function () {
        $scope.UpdateSuccess = false;
        $scope.Error = false;
        var btn = $("#btnUpdate");
        btn.button('loading');
        $http.post('/ChangePassword', $scope.User).success(function (result) {
            if (result.Updated) {
                $scope.UpdateSuccess = true;
                $scope.Error = false;
            }
            else {
                $scope.UpdateSuccess = false;
                $scope.Error = true;
            }
            btn.button('reset');
        });
    }
}

function UserManagementCtrl($scope, $http) {
    $scope.Success = false;
    $scope.UserList = [];
    $scope.Query = { PageNo: 1, Word: '', Status: -1, RowCount: 0, PageCount: 0 };
    $scope.query = function () {
        var btn = $("#btnQuery");
        btn.button('loading');
        $http.post('/QueryUser', $scope.Query).success(function (result) {
            btn.button('reset');
            $scope.UserList = result.data;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }
    $scope.enable = function (userid) {
        $scope.Success = false;
        $http.post('/EnableUser', { UserId: userid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.disable = function (userid) {
        $scope.Success = false;
        $http.post('/DisableUser', { UserId: userid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.resetpass = function (userid) {
        $scope.Success = false;
        $http.post('/ResetPassword', { UserId: userid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.assignadmin = function (userid) {
        $scope.Success = false;
        $http.post('/AssignAdmin', { UserId: userid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
}

function CategoryCtrl($scope, $http) {
    $scope.Success = false;
    $scope.Exist = false;
    $scope.CategoryList = [];
    $scope.query = function () {
        $http.post('/QueryCategory').success(function (result) {
            $scope.CategoryList = result.data;
        });
    }
    $scope.enable = function (categoryid) {
        $scope.Success = false;
        $http.post('/EnableCategory', { CategoryId: categoryid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.disable = function (categoryid) {
        $scope.Success = false;
        $http.post('/DisableCategory', { CategoryId: categoryid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.create = function () {
        $scope.Success = false;
        $scope.Exist = false;
        $http.post('/CreateCategory', { CategoryName: $scope.CategoryName }).success(function (result) {
            if (result.status) {
                $scope.Success = false;
                $scope.Exist = true;
            } else {
                $scope.Success = true;
                $scope.Exist = false;
            }
            $scope.query();
        });
    }
}

//function RepositoryCtrl($scope, $http) {
//    $scope.Success = false;
//    $scope.Exist = false;
//    $scope.RepositoryList = [];
//    $scope.query = function () {
//        $http.post('/QueryRepository').success(function (result) {
//            $scope.RepositoryList = result.data;
//        });
//    }
//    $scope.create = function () {
//        $scope.Success = false;
//        $scope.Exist = false;
//        $http.post('/CreateRepository', { RepositoryName: $scope.RepositoryName }).success(function (result) {
//            if (result.status) {
//                $scope.Success = false;
//                $scope.Exist = true;
//            } else {
//                $scope.Success = true;
//                $scope.Exist = false;
//            }
//            $scope.query();
//        });
//    }
//    $scope.RemoveRepository = function (RepositoryId) {
//        $scope.AddSuccess = false;
//        $scope.RemoveSuccess = false;
//        $http.post('/RemoveRepository', {'RepositoryId': RepositoryId }).success(function (result) {
//            if (result.removed) {
//                $scope.RemoveSuccess = true;
//                $scope.query();
//                window.location.href = "/Admin/RepositorySetting" 
//                
//            }
//        });
//    }
//}

function RepositoryCategoryCtrl($scope, $http) {
    $scope.Success = false;
    $scope.Exist = false;
    $scope.Platform = {}
    $scope.RepositoryCategoryList = [];
    $scope.query = function () {
        $http.post('/QueryRepositoryCategory',{"ProjectId": $scope.ProjectId}).success(function (result) {
            $scope.RepositoryCategoryList = result.data;
        });
    }
    $scope.create = function () {
        $scope.Success = false;
        $scope.Exist = false;
        $http.post('/CreateRepositoryCategory', {ProjectId: $scope.ProjectId,RepositoryCategoryName: $scope.RepositoryCategoryName }).success(function (result) {
            if (result.status) {
                $scope.Success = false;
                $scope.Exist = true;
            } else {
                $scope.Success = true;
                $scope.Exist = false;
            }
//            $scope.RepositoryId=result.RepositoryId
            $scope.query();
        });
    }
    $scope.RemoveRepositoryCategory = function (RepositoryCategoryId) {
        $scope.AddSuccess = false;
        $scope.RemoveSuccess = false;
        $http.post('/RemoveRepositoryCategory', {'ProjectId': $scope.ProjectId,'RepositoryCategoryId': RepositoryCategoryId }).success(function (result) {
            if (result.removed) {
                $scope.RemoveSuccess = true;
                $scope.query();
                
            }
        });
    }
    $scope.ConfigRepositoryCategory = function () {
        $http.post('/ConfigRepositoryCategory',{RepositoryCategoryId:$scope.RepositoryCategoryId,'CMPlatform':$scope.CMPlatform,'CIPlatform':$scope.CIPlatform,'ReposPlatform':$scope.ReposPlatform}).success(function (result) {
        
        });
    }
}

function RequirementCtrl($scope, $http) {
    $scope.Success = false;
    $scope.Exist = false;
    editor = UE.getEditor('editor');
    $scope.RequirementList = [];
    $scope.Query = { PageNo: 1, RequirementName: '', Versions: '', Introduction: '', Status: 1, RowCount: 0, PageCount: 0 };
    $scope.query = function () {
        $http.post('/Requirement/Query',{'RequirementId': $scope.RequirementId,'Status': $scope.Query.Status,'PageNo':$scope.Query.PageNo }).success(function (result) {
            $scope.RequirementList = result.data;
            $scope.RequirementList2 = result.data2;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
//            window.location.href = '/Requirement';
        });
    }
    $scope.create = function () {
        $scope.Success = false;
        $scope.Exist = false;
        $scope.Description = editor.getContent();
        $http.post('/CreateRequirement',{RequirementName: $scope.RequirementName,Versions: $scope.Versions,Description:$scope.Description }).success(function (result) {
            if (result.status) {
                $scope.Success = false;
                $scope.Exist = true;
            } else {
                $scope.Success = true;
                $scope.Exist = false;
            }
            window.location.href = '/Requirement';
            $scope.query();
        });
    }
} 

function RequirementUpdateCtrl($scope, $http) {
	$scope.ShowUpdate = true;
    $scope.edit = function () {

        $scope.ShowUpdate = !$scope.ShowUpdate;
        UE.getEditor('editor1');
       
    }
    $scope.update = function () {
    	  
            var btn = $("#btnUpdate");
            btn.button('loading');
            UE.getEditor('editor1').hasContents()
            $scope.Description = UE.getEditor('editor1').getContent();
            $http.post('/Requirement/Update', {'RequirementId':$scope.RequirementId , "RequirementName": $scope.RequirementName,"Versions": $scope.Versions,"Description":$scope.Description,"Status":$scope.Status }).success(function (result) {
                if (result.updated) {
                    $scope.UpdateSuccess = true;
                    btn.button('reset');
                    window.location.href = '/Requirement';
                }
            });
        
    }
}
function ThemeItemCtrl($scope, $http) {
	$scope.Success = false;
    $scope.Exist = false;
    $scope.query = function () {
        $http.post('/QueryThemeItem').success(function (result) { 
        	$scope.ThemeItemList = result.data;
        });
    }
    $scope.create = function () {
        $scope.Success = false;
        $scope.Exist = false;
        $http.post('/CreateThemeItem',{'ThemeItemName': $scope.ThemeItemName}).success(function (result) {
            if (result.status) {
                $scope.Success = false;
                $scope.Exist = true;
            } else {
                $scope.Success = true;
                $scope.Exist = false;
            }
            window.location.href = '/Item';
            $scope.query();
        });
    }
}   
function ItemCtrl($scope, $http) {
	$scope.SunItem ={};
	$scope.Success = false;
    $scope.Exist = false;
    $scope.ShowUE = false;
    var itemDescription=[];
    var sunitemnamelist=[];
    $scope.query = function () {
        $http.post('/QueryItem',{'ThemeItemId': $scope.Item.ThemeItemId}).success(function (result) { 
        	$scope.ItemList = result.data;
//        	alert($scope.ItemList)
        });
    }
    $scope.create = function () {
        $scope.Success = false;
        $scope.Exist = false;
//        alert(counter);
        for (var i=1;i<=counter;i++)
        {
        var value = document.getElementById(i+"item").value;
        var sHTML = $('#'+i).eq(1).code();
        sunitemnamelist.push(value);
        itemDescription.push($('#'+i).code(sHTML));
        }
        $scope.SunItem.SunItemName = sunitemnamelist
        $scope.SunItem.Description = itemDescription;
        $scope.Item.Description = $('#0').code(sHTML);
//        alert($scope.SunItem.Description)
//        alert($scope.SunItem)
        $http.post('/CreateItem',{"Item":$scope.Item,"SunItem":$scope.SunItem}).success(function (result) {
            if (result.status) {
                $scope.Success = false;
                $scope.Exist = true;
            } else {
                $scope.Success = true;
                $scope.Exist = false;
            }
            $scope.detail($scope.Item.ThemeItemId);
        });
    }
    $scope.addItem = function () {

    	counter++;
        x.push(counter);
        $scope.things=x;

    }
    $scope.delItem = function (){
        x.pop();
        $scope.things=x;
        counter--;
    }
    $scope.$on('ngRepeatFinished', function (ngRepeatFinishedEvent) {
        //下面是在table render完成后执行的js

        $(document).ready(function() {
            [$('#'+counter).summernote()];
        
         });

    });

} 

//    $scope.RemoveRequirement = function (RequirementId) {
//        $scope.AddSuccess = false;
//        $scope.RemoveSuccess = false;
//        $http.post('/RemoveRequirement', {'RequirementId': RequirementId }).success(function (result) {
//            if (result.removed) {
//                $scope.RemoveSuccess = true;
//                $scope.query();
//                window.location.href = '/Requirement';
//                
//            }
//        });
//    }
//}

//    $scope.RemoveRepository = function (RepositoryId) {
//        $scope.AddSuccess = false;
//        $scope.RemoveSuccess = false;
//        $http.post('/RemoveRepository', {'RepositoryId': RepositoryId }).success(function (result) {
//            if (result.removed) {
//                $scope.RemoveSuccess = true;
//                $scope.query();
//                window.location.href = "/Admin/RepositorySetting" 
//                
//            }
//        });
//    }
//}

function NoticeCtrl($scope, $http) {
    $scope.Query = { Content: '' };
    $scope.create = function () {
        var btn = $("#btnCreateNotice");
        btn.button('loading');
        $http.post('/Notice/Create', $scope.Notice).success(function (result) {
            btn.button('reset');
            if (result.created) {
                $('#notice_add').modal('hide');
                $scope.query();
            }
        });
    }
    $scope.query = function () {
        var btn = $("#btnQueryNotice");
        btn.button('loading');
        $scope.isEmpty = true;
        $http.post('/Notice/Query').success(function (result) {
            btn.button('reset');
            $scope.NoticeList = result.data;
            $scope.isEmpty = false;
        });
    }
}

function HistoryCtrl($scope, $http) {
    $scope.HistoryList = [];
    $scope.Query = { PageNo: 1, PageCount: 0, RowCount: 0 };
    $scope.query = function () {
        $http.post('/History', $scope.Query).success(function (result) {
            $scope.HistoryList = result.data;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }
}

function CommentCtrl($scope, $http) {
    $scope.CommentList = [];
    $scope.Query = { PageNo: 1, PageCount: 0, RowCount: 0 };
    $scope.isSuccess = false
    $scope.create = function () {
        var btn = $("#btnCreateComment");
        btn.button('loading');
        if ($scope.Comment.Content != '') {
	        $http.post('/Comment/Create', $scope.Comment).success(function (result) {
	            btn.button('reset');
	            if (result.created) {
	                $("#new_commnet").collapse("hide");
	                $scope.Comment.Content = '';            //每次成功新建后，清除内容
	                $scope.isSuccess = true;
	                $scope.thiscomment = result.comment_id;
	                $scope.query();
	            }
	        });
		}
		else {
			alert("请输入评论内容！");
			btn.button('reset');
		}

    }
    $scope.query = function () {
        $http.post('/Comment/Query', $scope.Query).success(function (result) {
            $scope.CommentList = result.data;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }
}


function SubCommentCtrl($scope, $http) {
    $scope.SubQuery = { PageNo: 1, PageCount: 0, RowCount: 0 };
    $scope.create_sub = function () {
        var btn = $("#btnCreateSubComment");
        btn.button('loading');
        if ($scope.SubComment.Content != '') {
	        $http.post('/SubComment/Create', $scope.SubComment).success(function (result) {
	            btn.button('reset');
	            if (result.created) {
	                $("#sub_comment"+$scope.collapse).collapse("hide");     //新建后，收回评论输入框
	                $scope.SubComment.Content = '';            //每次成功新建后，清除内容
	                //$scope.isSuccess = true;
	                //$scope.thiscomment = result.comment_id;
	                $scope.query_sub();
	            }
	        });
	    }
	    else {
	    	alert("请输入评论内容！");
			btn.button('reset');
	    }
    }
    $scope.ReplySubComment = {};
    $scope.reply_sub = function () {
        var btn = $("#btnReplySubComment");
        btn.button('loading');
        if ($scope.ReplySubComment.ReplyContent != '') {
	        $http.post('/SubComment/Reply', $scope.ReplySubComment).success(function (result) {
	            btn.button('reset');
	            if (result.created) {
	                //$("#sub_commnet*").collapse("hide");     //新建后，收回评论输入框，由于涉及变量，暂时未能实现
	                $scope.ReplySubComment.ReplyContent = '';            //每次成功新建后，清除内容
	                //$scope.isSuccess = true;
	                //$scope.thiscomment = result.comment_id;
	                $scope.query_sub();
	            }
	        });
	    }
	    else {
	    	alert("请输入评论内容！");
			btn.button('reset');
	    }
    }
    $scope.query_sub = function () {
        $http.post('/SubComment/Query', $scope.SubQuery).success(function (result) {
            $scope.SubCommentList = result.data;
            $scope.SubQuery.RowCount = result.row_count;
            $scope.SubQuery.PageCount = result.page_count;
            $scope.SubQuery.PageNo = result.page_no;
        });
    }
}


function onChange( obj )
{
    if(obj == "ProjectKey")
    /*用于验证ProjectKey的输入是否符合规范*/
        {
            document.getElementById("message").innerHTML="";
            document.getElementById("btnCreateProject").disabled=false;
            var keyObj = document.getElementById(obj);
            var key = new String(keyObj.value);
            if( (key.length > 255) )
            {
                document.getElementById("message").innerHTML="key值不能超过255个字符";
            }
            var Regex = /^([a-zA-Z0-9])+$/;

            if (!Regex.test(key))
            {                
                document.getElementById("message").innerHTML = "输入格式不正确，请重新输入；";                    
                document.getElementById("btnCreateProject").disabled=true; 
                //keyObj.value = "";
                return false;            
            }            
            
            /*
            for (i=0; i<key.length; i++)
            {
                if (key.charAt(i) != "/^([a-zA-Z0-9])+@([a-zA-Z0-9])+([a-zA-Z0-9])+/")
                    {
                        document.getElementById("message").innerHTML="key值输入格式不对";
                        return false;
                    }
            }
            */
        }
}

//function addRow(tbodyID)  
//{  
//
//	var bodyObj=document.getElementById(tbodyID);  
//    if(bodyObj==null)   
//    {  
//        alert("Body of Table not Exist!");  
//        return;  
//    }  
//    var rowCount = bodyObj.rows.length;  
//    var cellCount = bodyObj.rows[0].cells.length;  
//    var newRow = bodyObj.insertRow(rowCount++);    
//    for(var i=0;i<cellCount;i++)  
//    {    
//
//    	 var cellHTML = bodyObj.rows[0].cells[i].innerHTML;  
//         if(cellHTML.indexOf("none")>=0)  
//         {  
//        	
//        	 cellHTML = cellHTML.replace("none","");  
//         } 
//         if(cellHTML.indexOf("SunItemName")>=0)  
//         {  
//        	
//        	 SunItemName="SunItemName"+rowCount
//        	 y=x.push(SunItemName)
//        	 
//        	 cellHTML = cellHTML.replace("SunItemName","SunItemName"+rowCount);  
//
//         }
//         newRow.insertCell(i).innerHTML=cellHTML;  
//    } 
//    alert(x)
//    return x
    
//}  
//function removeRow(inputobj)  
//{  
//    if(inputobj==null) return;  
//    var parentTD = inputobj.parentNode;  
//    var parentTR = parentTD.parentNode;  
//    var parentTBODY = parentTR.parentNode;  
//    parentTBODY.removeChild(parentTR);  
//}



function  getInfo() 
{ 
var s = ""; 
s += " 网页可见区域宽："+ document.body.clientWidth + "\n";
s += " 网页可见区域高："+ document.body.clientHeight + "\n"; 
s += " 网页可见区域宽："+  document.body.offsetWidth + " (包括边线和滚动条的宽)" + "\n"; 
s += " 网页可见区域高："+  document.body.offsetHeight + " (包括边线的宽)" + "\n"; 
s += " 网页正文全文宽："+  document.body.scrollWidth + "\n"; 
s += " 网页正文全文高："+ document.body.scrollHeight + "\n";  
s += " 网页被卷去的高(ff)："+ document.body.scrollTop + "\n"; 
s += " 网页被卷去的高(ie)："+  document.documentElement.scrollTop + "\n"; 
s += " 网页被卷去的左："+  document.body.scrollLeft + "\n"; 
s += " 网页正文部分上："+ window.screenTop + "\n"; 
s += " 网页正文部分左："+ window.screenLeft + "\n"; 
s += " 屏幕分辨率的高："+ window.screen.height + "\n"; 
s += " 屏幕分辨率的宽："+ window.screen.width + "\n"; 
s += " 屏幕可用工作区高度："+  window.screen.availHeight + "\n"; 
s += " 屏幕可用工作区宽度："+ window.screen.availWidth + "\n";  
s += " 你的屏幕设置是 "+ window.screen.colorDepth +" 位彩色" + "\n"; 
s += " 你的屏幕设置 "+  window.screen.deviceXDPI +" 像素/英寸" + "\n"; 
alert (s); 
} 

function GetHeight()
{
	s = document.body.clientHeight;
	
	return s;
}


