require 'rake'
require 'erb'

desc "install the dot files into user's home directory"
task :install do |t, args|
  Dir['*'].each do |file|
    next if %w[Rakefile README.rdoc README.md LICENSE].include? file

    if File.exist?(File.join(ENV['HOME'], ".#{file.sub('.erb', '')}"))
      if File.identical? file, File.join(ENV['HOME'], ".#{file.sub('.erb', '')}")
        puts "identical ~/.#{file.sub('.erb', '')}"
      else
        replace_file(file)
      end
    else
      link_file(file)
    end
  end

  unless Dir.exist?(File.join(ENV['HOME'], ".oh-my-zsh"))
    puts "Installing oh-my-zsh"
    system %Q{git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh}
  end
end

def replace_file(file)
  system %Q{rm -rf "$HOME/.#{file.sub('.erb', '')}"}
  link_file(file)
end

def link_file(file)
  if file =~ /.erb$/
    puts "generating ~/.#{file.sub('.erb', '')}"
    File.open(File.join(ENV['HOME'], ".#{file.sub('.erb', '')}"), 'w') do |new_file|
      new_file.write ERB.new(File.read(file)).result(binding)
    end
  else
    puts "linking ~/.#{file}"
    system %Q{ln -s "$PWD/#{file}" "$HOME/.#{file}"}
  end
end
