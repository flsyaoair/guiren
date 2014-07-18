﻿var app = angular.module('PowerTeam', []);

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

$(function () {
    $('input, textarea').placeholder();
    $('.default-focus').focus();
    $('*').tooltip({
        selector: "[data-toggle=tooltip]",
        container: "body"
    });
});

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
    $scope.Query = { PageNo: 1, ProjectName: '', Status: 1, RowCount: 0, PageCount: 0 };
    $scope.create = function () {
        var btn = $("#btnCreateProject");
        btn.button('loading');
        $http.post('/Project/Create', $scope.Project).success(function (result) {
            btn.button('reset');
            if (result.created) {
                $('#project_add').modal('hide');
                $scope.query();
            }
        });
    }
    $scope.query = function () {
        var btn = $("#btnQuery");
        btn.button('loading');
        $http.post('/Project/Query', $scope.Query).success(function (result) {
            btn.button('reset');
            $scope.ProjectList = result.data;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
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
    $scope.Query = { PageNo: 1, TaskName: '', AssignTo: -1, New: true, InProgress: true, Completed: false, Canceled: false, RowCount: 0, PageCount: 0 };
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
    $scope.Task = { TaskName: null, Priority: 2, AssignTo: -1, Description: null };
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
    editor = UE.getEditor('editor');
    $scope.update = function () {
        var btn = $("#btnUpdate");
        btn.button('loading');
        $scope.Task.Description = editor.getContent();
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
    $scope.Issue = { Subject: null, AssignTo: -1, Priority: 2, Description: null, CategoryId: -1 };
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